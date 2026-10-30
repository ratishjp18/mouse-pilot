"""
Tests for Scheduler
"""

import pytest
from datetime import datetime, timedelta
from PySide6.QtCore import QCoreApplication
from services.scheduler import Scheduler


@pytest.fixture
def qt_app():
    """Create QCoreApplication for testing"""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return app


def test_scheduler_initialization(qt_app):
    """Test scheduler initializes correctly"""
    scheduler = Scheduler()
    assert not scheduler.is_running
    assert not scheduler.is_paused
    assert scheduler.interval_seconds == 60


def test_scheduler_start_stop(qt_app):
    """Test starting and stopping scheduler"""
    scheduler = Scheduler()
    
    scheduler.start(30)
    assert scheduler.is_running
    assert not scheduler.is_paused
    assert scheduler.interval_seconds == 30
    
    scheduler.stop()
    assert not scheduler.is_running
    assert not scheduler.is_paused


def test_scheduler_pause_resume(qt_app):
    """Test pausing and resuming scheduler"""
    scheduler = Scheduler()
    
    scheduler.start(30)
    assert scheduler.is_running
    
    scheduler.pause()
    assert scheduler.is_running
    assert scheduler.is_paused
    
    scheduler.resume()
    assert scheduler.is_running
    assert not scheduler.is_paused


def test_scheduler_interval_change(qt_app):
    """Test changing interval while running"""
    scheduler = Scheduler()
    
    scheduler.start(30)
    assert scheduler.interval_seconds == 30
    
    scheduler.set_interval(60)
    assert scheduler.interval_seconds == 60
    assert scheduler.is_running
