import json
import unittest

from link_rep import LinkId, LinkRep, LinkTerm, VarDef


DOCUMENT = """//example
K3a1: [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
[K3a1, K3a1]
L[1, 1]#L[2, 1]
"""


class LinkRepresentationTests(unittest.TestCase):
    def test_text_and_json_round_trip(self):
        representation = LinkRep()
        representation.deserialize(DOCUMENT)
        self.assertEqual(representation.serialize(), DOCUMENT)
        clone = LinkRep()
        clone.json_deserialize(representation.json_serialize())
        self.assertEqual(clone.serialize(), DOCUMENT)

    def test_reused_link_id_resets_mirror_state(self):
        link_id = LinkId()
        link_id.deserialize("mK3a1")
        self.assertTrue(link_id.mirror)
        link_id.deserialize("K4a1")
        self.assertFalse(link_id.mirror)
        self.assertEqual(link_id.serialize(), "K4a1")

    def test_join_indices_must_be_positive_non_boolean_integers(self):
        for text in ("L[0, 1]#L[2, 1]", "L[1, -1]#L[2, 1]"):
            with self.assertRaisesRegex(ValueError, "positive"):
                LinkTerm().deserialize(text)
        with self.assertRaisesRegex(ValueError, "positive"):
            LinkTerm().json_deserialize(
                json.dumps(
                    {"type": "LinkTerm", "component_list": [[True, 1], [2, 1]]}
                )
            )

    def test_duplicate_or_invalid_pd_definitions_are_rejected(self):
        duplicate = DOCUMENT.replace("[K3a1, K3a1]", "K3a1: []\n[K3a1]")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            LinkRep().deserialize(duplicate)
        with self.assertRaisesRegex(ValueError, "invalid PD"):
            VarDef().deserialize("K3a1: [[1, 2, 3, 4]]")

    def test_empty_factor_set_parses_but_full_evaluator_can_reject_it(self):
        representation = LinkRep()
        representation.deserialize("[]")
        self.assertEqual(representation.link_set.var_list, [])


if __name__ == "__main__":
    unittest.main()
