# -*- coding: utf-8 -*-

import pytest
from tests.utils import Rule, CorrectedCommand
from thefuck import corrector, const
from thefuck.system import Path
from thefuck.types import Command
from thefuck.corrector import get_corrected_commands, organize_commands
from thefuck.entrypoints.main import setUID
import platform


class TestGetRules(object):
    @pytest.fixture
    def glob(self, mocker):
        results = {}
        mocker.patch('thefuck.system.Path.glob',
                     new_callable=lambda: lambda *_: results.pop('value', []))
        return lambda value: results.update({'value': value})

    @pytest.fixture(autouse=True)
    def load_source(self, monkeypatch):
        monkeypatch.setattr('thefuck.types.load_source',
                            lambda x, _: Rule(x))

    def _compare_names(self, rules, names):
        assert {r.name for r in rules} == set(names)

    @pytest.mark.parametrize('paths, conf_rules, exclude_rules, loaded_rules', [
        (['git.py', 'bash.py'], const.DEFAULT_RULES, [], ['git', 'bash']),
        (['git.py', 'bash.py'], ['git'], [], ['git']),
        (['git.py', 'bash.py'], const.DEFAULT_RULES, ['git'], ['bash']),
        (['git.py', 'bash.py'], ['git'], ['git'], [])])
    def test_get_rules(self, glob, settings, paths, conf_rules, exclude_rules,
                       loaded_rules):
        glob([Path(path) for path in paths])
        settings.update(rules=conf_rules,
                        priority={},
                        exclude_rules=exclude_rules)
        rules = corrector.get_rules()
        self._compare_names(rules, loaded_rules)


def test_get_corrected_commands(mocker):
    command = Command('test', 'test')
    rules = [Rule(match=lambda _: False),
             Rule(match=lambda _: True,
                  get_new_command=lambda x: x.script + '!', priority=100),
             Rule(match=lambda _: True,
                  get_new_command=lambda x: [x.script + '@', x.script + ';'],
                  priority=60)]
    mocker.patch('thefuck.corrector.get_rules', return_value=rules)
    assert ([cmd.script for cmd in get_corrected_commands(command)]
            == ['test!', 'test@', 'test;'])


def test_organize_commands():
    """Ensures that the function removes duplicates and sorts commands."""
    commands = [CorrectedCommand('ls'), CorrectedCommand('ls -la', priority=9000),
                CorrectedCommand('ls -lh', priority=100),
                CorrectedCommand(u'echo café', priority=200),
                CorrectedCommand('ls -lh', priority=9999)]
    assert list(organize_commands(iter(commands))) \
        == [CorrectedCommand('ls'), CorrectedCommand('ls -lh', priority=100),
            CorrectedCommand(u'echo café', priority=200),
            CorrectedCommand('ls -la', priority=9000)]


@pytest.mark.skipif(platform.system() != 'Linux', reason='Requires Linux')
@pytest.mark.parametrize('command, uid, result', [
    (Command('sudo apt-get instll flask8', 'E: Invalid operation instll'), 1234, 'sudo apt-get install flask8'),
    (Command('apt-get instll flask8', 'E: Invalid operation instll'), 0, 'apt-get install flask8')])
def test_get_correct_command(command, uid, result):
    setUID(uid)
    corrected_commands = list(get_corrected_commands(command))
    assert len(corrected_commands) > 0
    assert(corrected_commands[0].script == result)


@pytest.mark.parametrize('command', [
    (Command('sudo jubberish sodasudaosu', 'E: Invalid operation instll')), ])
def test_no_commands_found(command):
    corrected_commands = list(get_corrected_commands(command))
    assert len(corrected_commands) == 0


@pytest.mark.skipif(platform.system() != 'Linux', reason='Requires Linux')
@pytest.mark.parametrize('command, result', [
    (Command('apt-get instll flask8', 'E: Invalid operation instll'), 'sudo apt-get install flask8')])
def test_none_root_commands(command, result):
    setUID(1234)
    corrected_commands = list(get_corrected_commands(command))
    assert len(corrected_commands) > 0
    assert(result in [corrected.script for corrected in corrected_commands])
