import copy
import unittest
from typing import List, Dict, Callable

from model.achievement import Achievement
from model.guild_manager import GuildManager, GuildMember
from model.inventory.exceptions.inventory_contains_item_error import InventoryContainsItemError
from model.inventory.inventory import Inventory
from model.person import Person


class TestGuildManager(unittest.TestCase):
    guild: Inventory[Person]
    guild_manager: GuildManager

    MEMBER_ID_A = "Member A"
    MEMBER_ID_B = "Member B"
    MEMBER_ID_C = "Member C"

    MEMBER_DISPLAY_NAME_A = "Member A Display Name"
    MEMBER_DISPLAY_NAME_B = "Member B Display Name"
    MEMBER_DISPLAY_NAME_C = "Member C Display Name"

    member_a: GuildMember
    member_b: GuildMember
    member_c: GuildMember

    ACHIEVEMENT_NAME_A = "Achievement A"
    ACHIEVEMENT_NAME_B = "Achievement B"
    ACHIEVEMENT_NAME_C = "Achievement C"

    def setUp(self) -> None:
        self.guild = Inventory[Person]()
        self.guild_manager = GuildManager(self.guild)

        self.member_a = GuildMember(self.MEMBER_ID_A, self.MEMBER_DISPLAY_NAME_A)
        self.member_b = GuildMember(self.MEMBER_ID_B, self.MEMBER_DISPLAY_NAME_B)
        self.member_c = GuildMember(self.MEMBER_ID_C, self.MEMBER_DISPLAY_NAME_C)

    def assert_guild_members_state(self, expected_guild_members: List[GuildMember]):
        self.assertEqual(len(expected_guild_members), self.guild_manager.guild_size())

        self.assertEqual(self.member_a in expected_guild_members,
                         self.guild_manager.guild_contains(self.MEMBER_ID_A))

        self.assertEqual(self.member_b in expected_guild_members,
                         self.guild_manager.guild_contains(self.MEMBER_ID_B))

        self.assertEqual(self.member_c in expected_guild_members,
                         self.guild_manager.guild_contains(self.MEMBER_ID_C))

    def test_init(self):
        self.assert_guild_members_state([])

    def assert_achievements(self, expected_achievements: List[Achievement], actual_achievements: List[Achievement]):

        # NOTE: Expected achievements' bestower values are irrelevant
        self.assertEqual(len(expected_achievements), len(actual_achievements))

        for i in range(len(expected_achievements)):
            self.assertEqual(expected_achievements[i].name, actual_achievements[i].name)

    def assert_guild_member_achievements_state(self, expected_state: Dict[GuildMember, List[Achievement]]):
        self.assert_guild_members_state(list(expected_state.keys()))

        for expected_guild_member, expected_achievements in expected_state.items():
            actual_person = self.guild.get(expected_guild_member.id)
            actual_achievements = actual_person.get_achievements()

            self.assert_achievements(expected_achievements, actual_achievements)

    def assert_add_achievement_pass(self,
                                    member: GuildMember,
                                    valid_members: List[GuildMember],
                                    achievement_name: str,
                                    bestower: str,
                                    expected_state_pre_pass: Dict[GuildMember, List[Achievement]]):
        try:
            achievement = Achievement(achievement_name, bestower)
            self.guild_manager.add_achievement(member, valid_members, achievement)
            actual_person = self.guild.get(member.id)
            actual_achievement = actual_person.get(achievement_name)
            self.assertEqual(achievement_name, actual_achievement.name)
        except ValueError:
            self.fail()
        except InventoryContainsItemError:
            self.fail()

        expected_state = expected_state_pre_pass
        added_achievement = Achievement(achievement_name, "")

        if member in expected_state.keys():
            expected_state[member].append(added_achievement)
        else:
            expected_state[member] = [added_achievement]

        self.assert_guild_member_achievements_state(expected_state)

    def assert_add_achievement_value_error(self,
                                           member: GuildMember,
                                           valid_members: List[GuildMember],
                                           achievement_name: str,
                                           bestower: str,
                                           expected_state: Dict[GuildMember, List[Achievement]]):
        try:
            achievement = Achievement(achievement_name, bestower)
            self.guild_manager.add_achievement(member, valid_members, achievement)
            self.fail()
        except ValueError:
            pass
        except InventoryContainsItemError:
            self.fail()

        self.assert_guild_member_achievements_state(expected_state)

    def assert_add_achievement_inventory_error(self,
                                               member: GuildMember,
                                               valid_members: List[GuildMember],
                                               achievement_name: str,
                                               bestower: str,
                                               expected_state: Dict[GuildMember, List[Achievement]]):
        try:
            achievement = Achievement(achievement_name, bestower)
            self.guild_manager.add_achievement(member, valid_members, achievement)
            self.fail()
        except ValueError:
            self.fail()
        except InventoryContainsItemError:
            pass

        self.assert_guild_member_achievements_state(expected_state)

    def assert_add_achievement_bestower_cases(self,
                                              member: GuildMember,
                                              valid_members: List[GuildMember],
                                              achievement_name: str,
                                              expected_state: Dict[GuildMember, List[Achievement]],
                                              member_is_not_bestower_assertion: Callable[[GuildMember,
                                                                                          List[GuildMember],
                                                                                          str,
                                                                                          str,
                                                                                          Dict[GuildMember,
                                                                                               List[
                                                                                                   Achievement]]],
                                                                                         None]):
        # Member is Bestower
        self.assert_add_achievement_value_error(member, valid_members, achievement_name, member.id, expected_state)

        # Member is not Bestower
        member_is_not_bestower_assertion(member, valid_members, achievement_name, member.id + "x", expected_state)

    def assert_add_achievement_bestower_cases_external_value_error(self,
                                                                   member: GuildMember,
                                                                   valid_members: List[GuildMember],
                                                                   achievement_name: str,
                                                                   expected_state: Dict[
                                                                       GuildMember, List[Achievement]]):
        self.assert_add_achievement_bestower_cases(member,
                                                   valid_members,
                                                   achievement_name,
                                                   expected_state,
                                                   self.assert_add_achievement_value_error)

    def assert_add_achievement_input_cases(self,
                                           member: GuildMember,
                                           achievement_name: str,
                                           expected_state_pre_pass: Dict[GuildMember, List[Achievement]]):
        expected_state_pre_pass_copy = copy.deepcopy(expected_state_pre_pass)

        # Empty Valid Members
        valid_members = []
        self.assert_add_achievement_bestower_cases_external_value_error(member,
                                                                        valid_members,
                                                                        achievement_name,
                                                                        expected_state_pre_pass_copy)

        # Valid Members Doesn't Contain Member
        other_members = [self.member_a, self.member_b, self.member_c]
        other_members.remove(member)

        valid_members.append(other_members[0])
        self.assert_add_achievement_bestower_cases_external_value_error(member,
                                                                        valid_members,
                                                                        achievement_name,
                                                                        expected_state_pre_pass_copy)

        valid_members.append(other_members[1])
        self.assert_add_achievement_bestower_cases_external_value_error(member,
                                                                        valid_members,
                                                                        achievement_name,
                                                                        expected_state_pre_pass_copy)

        # Valid Members Contains Member
        valid_members.append(member)

        actual_achievement_names = []

        if self.guild.contains(member.id):
            actual_person = self.guild.get(member.id)
            actual_achievements = actual_person.get_achievements()
            actual_achievement_names = [actual_achievement.name for actual_achievement in actual_achievements]

        if achievement_name in actual_achievement_names:
            self.assert_add_achievement_bestower_cases(member,
                                                       valid_members,
                                                       achievement_name,
                                                       expected_state_pre_pass_copy,
                                                       self.assert_add_achievement_inventory_error)
        else:
            self.assert_add_achievement_bestower_cases(member,
                                                       valid_members,
                                                       achievement_name,
                                                       expected_state_pre_pass_copy,
                                                       self.assert_add_achievement_pass)

    def test_add_achievements_start_with_no_members(self):
        expected_state_pre_pass = {}
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_b] = [Achievement(self.ACHIEVEMENT_NAME_A, "")]
        self.assert_add_achievement_input_cases(self.member_a,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

    def test_add_achievements_start_with_members(self):
        self.guild_manager.query_guild(self.member_a, [self.member_a])
        self.guild_manager.query_guild(self.member_b, [self.member_b])

        expected_state_pre_pass = {self.member_a: [],
                                   self.member_b: []}

        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_b] = [Achievement(self.ACHIEVEMENT_NAME_A, "")]
        self.assert_add_achievement_input_cases(self.member_a,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

    def test_add_achievement_other_person_has_same_achievement_start_with_no_members(self):
        expected_state_pre_pass = {}

        self.assert_add_achievement_input_cases(self.member_a,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_a] = [Achievement(self.ACHIEVEMENT_NAME_C, "")]
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_b] = [Achievement(self.ACHIEVEMENT_NAME_C, "")]
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c] = [Achievement(self.ACHIEVEMENT_NAME_A, "")]
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

    def test_add_achievement_other_person_has_same_achievement_start_with_members(self):
        self.guild_manager.query_guild(self.member_a, [self.member_a])
        self.guild_manager.query_guild(self.member_b, [self.member_b])
        self.guild_manager.query_guild(self.member_c, [self.member_c])

        expected_state_pre_pass = {self.member_a: [],
                                   self.member_b: [],
                                   self.member_c: []}

        self.assert_add_achievement_input_cases(self.member_a,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_a] = [Achievement(self.ACHIEVEMENT_NAME_C, "")]
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_b] = [Achievement(self.ACHIEVEMENT_NAME_C, "")]
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c] = [Achievement(self.ACHIEVEMENT_NAME_A, "")]
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

    def test_add_achievement_already_has_achievement_start_with_no_members(self):
        expected_state_pre_pass = {}

        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c] = [Achievement(self.ACHIEVEMENT_NAME_C, "")]
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_B,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c].append(Achievement(self.ACHIEVEMENT_NAME_B, ""))
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_B,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_b] = [Achievement(self.ACHIEVEMENT_NAME_B, "")]
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_b].append(Achievement(self.ACHIEVEMENT_NAME_C, ""))
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_B,
                                                expected_state_pre_pass)

        self.assert_add_achievement_input_cases(self.member_a,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_a] = [Achievement(self.ACHIEVEMENT_NAME_A, "")]
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c].append(Achievement(self.ACHIEVEMENT_NAME_A, ""))
        self.assert_add_achievement_input_cases(self.member_a,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

    def test_add_achievement_already_has_achievement_start_with_members(self):
        self.guild_manager.query_guild(self.member_b, [self.member_b])
        self.guild_manager.query_guild(self.member_c, [self.member_c])

        expected_state_pre_pass = {self.member_b: [],
                                   self.member_c: []}

        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c] = [Achievement(self.ACHIEVEMENT_NAME_C, "")]
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_B,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c].append(Achievement(self.ACHIEVEMENT_NAME_B, ""))
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_B,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_b].append(Achievement(self.ACHIEVEMENT_NAME_B, ""))
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_C,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_b].append(Achievement(self.ACHIEVEMENT_NAME_C, ""))
        self.assert_add_achievement_input_cases(self.member_b,
                                                self.ACHIEVEMENT_NAME_B,
                                                expected_state_pre_pass)

        self.guild_manager.query_guild(self.member_a, [self.member_a])
        expected_state_pre_pass[self.member_a] = []

        self.assert_add_achievement_input_cases(self.member_a,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_a].append(Achievement(self.ACHIEVEMENT_NAME_A, ""))
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c].append(Achievement(self.ACHIEVEMENT_NAME_A, ""))
        self.assert_add_achievement_input_cases(self.member_a,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

    def test_add_achievement_already_has_achievement_others_have_nothing_start_with_no_members(self):
        expected_state_pre_pass = {}

        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c] = [Achievement(self.ACHIEVEMENT_NAME_A, "")]
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_B,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c].append(Achievement(self.ACHIEVEMENT_NAME_B, ""))
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

    def test_add_achievement_already_has_achievement_others_have_nothing_start_with_members(self):
        self.guild_manager.query_guild(self.member_b, [self.member_c, self.member_b, self.member_a])
        self.guild_manager.query_guild(self.member_c, [self.member_c, self.member_b, self.member_a])
        self.guild_manager.query_guild(self.member_a, [self.member_c, self.member_b, self.member_a])

        expected_state_pre_pass = {self.member_b: [],
                                   self.member_c: [],
                                   self.member_a: []}

        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c] = [Achievement(self.ACHIEVEMENT_NAME_A, "")]
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_B,
                                                expected_state_pre_pass)

        expected_state_pre_pass[self.member_c].append(Achievement(self.ACHIEVEMENT_NAME_B, ""))
        self.assert_add_achievement_input_cases(self.member_c,
                                                self.ACHIEVEMENT_NAME_A,
                                                expected_state_pre_pass)

    # TODO: write tests for get achievements method

    def test_get_achievements(self):
        def assert_pass(member: GuildMember,
                        valid_members: List[GuildMember],
                        expected_guild_members: List[GuildMember],
                        expected_achievements: List[Achievement]):
            try:
                actual_achievements = self.guild_manager.get_achievements(member, valid_members)
                self.assert_achievements(expected_achievements, actual_achievements)
            except ValueError:
                self.fail()

            self.assert_guild_members_state(expected_guild_members)

        def assert_fail(member: GuildMember,
                        valid_members: List[GuildMember],
                        expected_guild_members: List[GuildMember]):
            try:
                self.guild_manager.get_achievements(member, valid_members)
                self.fail()
            except ValueError:
                pass

            self.assert_guild_members_state(expected_guild_members)

        def assert_valid_members_cases(member: GuildMember,
                                       expected_guild_members_pre_pass: List[GuildMember],
                                       expected_achievements_post_pass: List[Achievement]):
            expected_guild_members_pre_pass_copy = copy.deepcopy(expected_guild_members_pre_pass)

            # Empty Valid Members
            valid_members = []
            assert_fail(member, valid_members, expected_guild_members_pre_pass_copy)

            # Valid Members Doesn't Contain Member
            other_members = [self.member_a, self.member_b, self.member_c]
            other_members.remove(member)

            valid_members.append(other_members[0])
            assert_fail(member, valid_members, expected_guild_members_pre_pass_copy)

            valid_members.append(other_members[1])
            assert_fail(member, valid_members, expected_guild_members_pre_pass_copy)

            # Valid Members Contains Member
            valid_members.append(member)

            expected_guild_members = expected_guild_members_pre_pass_copy

            if member not in expected_guild_members:
                expected_guild_members.append(member)

            assert_pass(member, valid_members, expected_guild_members, expected_achievements_post_pass)

        guild_members_pre_pass = []
        assert_valid_members_cases(self.member_a, guild_members_pre_pass, [])

        guild_members_pre_pass.append(self.member_a)
        achievement_a = Achievement(self.ACHIEVEMENT_NAME_A, "")
        self.guild_manager.add_achievement(self.member_a, [self.member_a], achievement_a)

        assert_valid_members_cases(self.member_a, guild_members_pre_pass, [achievement_a])
        assert_valid_members_cases(self.member_b, guild_members_pre_pass, [])

        guild_members_pre_pass.append(self.member_b)
        achievement_b = Achievement(self.ACHIEVEMENT_NAME_B, "")
        self.guild_manager.add_achievement(self.member_b, [self.member_b], achievement_b)
        self.guild_manager.add_achievement(self.member_b, [self.member_b], achievement_a)

        assert_valid_members_cases(self.member_b, guild_members_pre_pass, [achievement_b, achievement_a])
        assert_valid_members_cases(self.member_a, guild_members_pre_pass, [achievement_a])
        assert_valid_members_cases(self.member_b, guild_members_pre_pass, [achievement_b, achievement_a])
        assert_valid_members_cases(self.member_c, guild_members_pre_pass, [])

        guild_members_pre_pass.append(self.member_c)
        achievement_c = Achievement(self.ACHIEVEMENT_NAME_C, "")
        self.guild_manager.add_achievement(self.member_a, [self.member_a], achievement_c)
        self.guild_manager.add_achievement(self.member_c, [self.member_c], achievement_a)
        self.guild_manager.add_achievement(self.member_b, [self.member_b], achievement_c)

        assert_valid_members_cases(self.member_c, guild_members_pre_pass, [achievement_a])
        assert_valid_members_cases(self.member_b, guild_members_pre_pass, [achievement_b, achievement_a, achievement_c])
        assert_valid_members_cases(self.member_a, guild_members_pre_pass, [achievement_a, achievement_c])
        assert_valid_members_cases(self.member_c, guild_members_pre_pass, [achievement_a])


if __name__ == '__main__':
    unittest.main()
