import pytest

from typing import List
from sparrow.toolkit.kgraph.parser import *


def test_parser():

    text = "Trout is a wonderfully flavoured fish when it's on your plate. However, when it's in the river it's a voracious predator."
    res: List[str] = parse_text(text)    

    assert len(res) > 0
    assert isinstance(res, List)
    assert isinstance(res[0].page_content, str)    