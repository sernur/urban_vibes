# sector.py
class Sector:
    """
    Class to represent a sector of interest for monitoring social media content.
    Attributes:
    - sector: str, the name of the sector
    - departments: list of str, departments responsible for that sector
    """
    def __init__(self, sector, departments):
        self.sector = sector
        self.departments = departments
