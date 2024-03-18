from __future__ import annotations
from enum import Enum


class UnitForceKind(Enum):
    """Force units"""

    DYNE_YOTTA = "Ydyn"
    """yotta Dyne 10/24"""
    DYNE_ZETTA = "Zdyn"
    """zetta Dyne 10/21"""
    DYNE_EXA = "Edyn"
    """exa 10/18"""
    DYNE_PETA = "Pdyn"
    """peta Dyne 10/15"""
    DYNE_TERA = "Tdyn"
    """tera Dyne 10/12"""
    DYNE_GIGA = "Gdyn"
    """giga Dyne 10/9"""
    DYNE_MEGA = "Mdyn"
    """mega Dyne 10/6"""
    DYNE_KILO = "kdyn"
    """kilo Dyne 10/3"""
    DYNE_HECTO = "hdyn"
    """hecto Dyne 10/2"""
    DYNE_DECA = "edyn"
    """deca Dyne 10/1"""
    DYNE = "dyn"
    """Dyne 10/0"""
    DYNE_DECI = "ddyn"
    """deci Dyne 10/-1"""
    DYNE_CENTI = "cdyn"
    """centi Dyne 10/-2"""
    DYNE_MILLI = "mdyn"
    """milli Dyne 10/-3"""
    DYNE_MICRO = "udyn"
    """micro Dyne 10/-6"""
    DYNE_NANO = "ndyn"
    """nano Dyne 10/-9"""
    DYNE_PICO = "pdyn"
    """pico Dyne 10/-12"""
    DYNE_FEMTO = "fdyn"
    """femto Dyne 10/-15"""
    DYNE_ATTO = "adyn"
    """atto Dyne 10/-18"""
    DYNE_ZEPTO = "zdyn"
    """zepto Dyne 10/-21"""
    DYNE_YOCTO = "ydyn"
    """yocto Dyne 10/-24"""
    NEWTON_YOTTA = "YN"
    """yotta Newton 10/24"""
    NEWTON_ZETTA = "ZN"
    """zetta Newton 10/21"""
    NEWTON_EXA = "EN"
    """exa 10/18"""
    NEWTON_PETA = "PN"
    """peta Newton 10/15"""
    NEWTON_TERA = "TN"
    """tera Newton 10/12"""
    NEWTON_GIGA = "GN"
    """giga Newton 10/9"""
    NEWTON_MEGA = "MN"
    """mega Newton 10/6"""
    NEWTON_KILO = "kN"
    """kilo Newton 10/3"""
    NEWTON_HECTO = "hN"
    """hecto Newton 10/2"""
    NEWTON_DECA = "eN"
    """deca Newton 10/1"""
    NEWTON = "N"
    """Newton 10/0"""
    NEWTON_DECI = "dN"
    """deci Newton 10/-1"""
    NEWTON_CENTI = "cN"
    """centi Newton 10/-2"""
    NEWTON_MILLI = "mN"
    """milli Newton 10/-3"""
    NEWTON_MICRO = "uN"
    """micro Newton 10/-6"""
    NEWTON_NANO = "nN"
    """nano Newton 10/-9"""
    NEWTON_PICO = "pN"
    """pico Newton 10/-12"""
    NEWTON_FEMTO = "fN"
    """femto Newton 10/-15"""
    NEWTON_ATTO = "aN"
    """atto Newton 10/-18"""
    NEWTON_ZEPTO = "zN"
    """zepto Newton 10/-21"""
    NEWTON_YOCTO = "yN"
    """yocto Newton 10/-24"""
    POUND_FORCE = "lbf"
    """pound force 10/0"""
    POND_YOTTA = "Ypond"
    """yotta Pond 10/24"""
    POND_ZETTA = "Zpond"
    """zetta Pond 10/21"""
    POND_EXA = "Epond"
    """exa 10/18"""
    POND_PETA = "Ppond"
    """peta Pond 10/15"""
    POND_TERA = "Tpond"
    """tera Pond 10/12"""
    POND_GIGA = "Gpond"
    """giga Pond 10/9"""
    POND_MEGA = "Mpond"
    """mega Pond 10/6"""
    POND_KILO = "kpond"
    """kilo Pond 10/3"""
    POND_HECTO = "hpond"
    """hecto Pond 10/2"""
    POND_DECA = "epond"
    """deca Pond 10/1"""
    POND = "pond"
    """Pond 10/0"""
    POND_DECI = "dpond"
    """deci Pond 10/-1"""
    POND_CENTI = "cpond"
    """centi Pond 10/-2"""
    POND_MILLI = "mpond"
    """milli Pond 10/-3"""
    POND_MICRO = "upond"
    """micro Pond 10/-6"""
    POND_NANO = "npond"
    """nano Pond 10/-9"""
    POND_PICO = "ppond"
    """pico Pond 10/-12"""
    POND_FEMTO = "fpond"
    """femto Pond 10/-15"""
    POND_ATTO = "apond"
    """atto Pond 10/-18"""
    POND_ZEPTO = "zpond"
    """zepto Pond 10/-21"""
    POND_YOCTO = "ypond"
    """yocto Pond 10/-24"""

    def __str__(self) -> str:
        return self.value
