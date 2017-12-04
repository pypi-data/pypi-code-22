#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sessionlib import Session, contextaware


def test_session_stack():
    s1 = Session()
    assert Session.current() == None

    with s1:
        assert Session.current() == s1

        with Session() as s2:
            assert Session.current() == s2

        assert Session.current() == s1

    assert Session.current() == None


def test_contextaware():
    @contextaware
    def aware_func(session):
        return session

    s1 = Session()

    assert aware_func() == None
    with s1:
        assert aware_func() == s1

        with Session() as s2:
            assert aware_func() == s2
            assert aware_func(s1) == s1
            assert aware_func() == s2

        assert aware_func() == s1

    assert aware_func() == None


def test_events(capsys):
    s1 = Session()
    s1.on_start.subscribe(lambda: print('start'))
    s1.on_enter.subscribe(lambda: print('enter'))
    s1.on_leave.subscribe(lambda: print('leave'))
    s1.on_close.subscribe(lambda: print('close'))

    with s1:
        with s1:
            pass

    out, _ = capsys.readouterr()
    assert out == 'start\nenter\nleave\nclose\n'
