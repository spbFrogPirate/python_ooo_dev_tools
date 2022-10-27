import sys
from ooodev.utils.file_io import FileIO
from pathlib import Path
from extract_text import ExtractText

# region maind()
def main() -> int:
    if len(sys.argv) == 2:
        fnm = sys.argv[1]
    else:
        fnm = "tests/fixtures/presentation/algs.odp"
        if not FileIO.is_exist_file(fnm):
            fnm = "../../../../tests/fixtures/presentation/algs.odp"
            FileIO.is_exist_file(fnm, True)
        fnm = Path("tests/fixtures/presentation/algs.odp")
    et = ExtractText(fnm)
    et.extract()
    return 0


# endregion maind()

if __name__ == "__main__":
    SystemExit(main())
