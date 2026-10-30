"""
Tests for Mouse Controller
"""

import pytest
from services.mouse_controller import MouseController


def test_mouse_controller_initialization():
    """Test mouse controller initializes correctly"""
    controller = MouseController()
    assert controller.last_position is None


def test_get_cursor_position():
    """Test getting cursor position"""
    controller = MouseController()
    pos = controller.get_cursor_position()
    
    assert isinstance(pos, tuple)
    assert len(pos) == 2
    assert isinstance(pos[0], int)
    assert isinstance(pos[1], int)


def test_get_screen_size():
    """Test getting screen size"""
    controller = MouseController()
    size = controller.get_screen_size()
    
    assert isinstance(size, tuple)
    assert len(size) == 2
    assert size[0] > 0
    assert size[1] > 0


def test_is_position_safe():
    """Test position safety checking"""
    controller = MouseController()
    screen_width, screen_height = controller.get_screen_size()
    
    # Test valid positions
    assert controller.is_position_safe(0, 0)
    assert controller.is_position_safe(100, 100)
    assert controller.is_position_safe(screen_width - 1, screen_height - 1)
    
    # Test invalid positions
    assert not controller.is_position_safe(-1, 0)
    assert not controller.is_position_safe(0, -1)
    assert not controller.is_position_safe(screen_width, screen_height)
    assert not controller.is_position_safe(screen_width + 100, screen_height + 100)
