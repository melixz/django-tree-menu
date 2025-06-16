from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Set

from django import template
from django.template import Context

from ..models import MenuItem

register = template.Library()


class _Node:
    """
    Вспомогательный класс для представления элемента меню в шаблоне.
    """

    def __init__(self, item: MenuItem):
        self.item = item
        self.children: List[_Node] = []
        self.is_open: bool = False
        self.is_active: bool = False

    @property
    def title(self) -> str:
        return self.item.title

    @property
    def url(self) -> str:
        return self.item.get_absolute_url()


@register.inclusion_tag("menu/draw_menu.html", takes_context=True)
def draw_menu(context: Context, menu_name: str):
    """
    Рисует древовидное меню с именем menu_name.
    """
    request = context["request"]
    current_path: str = request.path

    # Получаем все элементы меню одним запросом
    items: List[MenuItem] = list(
        MenuItem.objects.filter(menu__name=menu_name).select_related("parent", "menu")
    )
    if not items:
        return {"menu_root": []}

    # Формируем карту дочерних элементов: parent_id -> List[MenuItem]
    children_map: Dict[int | None, List[MenuItem]] = defaultdict(list)
    for item in items:
        children_map[item.parent_id].append(item)

    # Определяем активный элемент меню (по точному совпадению URL)
    active_item: MenuItem | None = next(
        (item for item in items if item.get_absolute_url() == current_path), None
    )

    # Собираем id всех раскрытых узлов (активный и его предки)
    open_nodes: Set[int] = set()
    if active_item is not None:
        current = active_item
        while current is not None:
            open_nodes.add(current.id)
            current = current.parent

    # Создаём объекты _Node для каждого элемента меню
    node_by_id: Dict[int, _Node] = {item.id: _Node(item) for item in items}
    for node in node_by_id.values():
        node.is_active = active_item is not None and node.item.id == active_item.id
        node.is_open = node.item.id in open_nodes

    # Формируем дерево: добавляем дочерние узлы
    for parent_id, children in children_map.items():
        if parent_id is None:
            continue
        parent_node = node_by_id[parent_id]
        for child_item in children:
            parent_node.children.append(node_by_id[child_item.id])

    # Корневые узлы (у которых нет родителя)
    root_nodes: List[_Node] = [node_by_id[item.id] for item in children_map[None]]

    # Гарантируем, что первый уровень потомков активного элемента всегда раскрыт
    if active_item is not None:
        for child in children_map.get(active_item.id, []):
            node_by_id[child.id].is_open = True

    return {"menu_root": root_nodes}
