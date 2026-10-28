import importlib.util,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validation',ROOT/'tools/validate.py');validation=importlib.util.module_from_spec(spec);spec.loader.exec_module(validation)
class TranslationDataTests(unittest.TestCase):
    def test_payload_integrity_and_subtitle_readability(self):validation.run()
