class OpenCageApiTypeError(Exception):
    def __str__(self) -> str:
        return """They OpenCage response was not the expected
                  Please use Locator.locate() for more"""


class ClimaCaseNoLocationError(Exception):
    def __str__(self) -> str:
        return "You have to pass coords or location param"


class ClimaAPIError(Exception):
    def __init__(self, resp):
        self.text = resp.text
        self.status_code = resp.status_code

    def __str__(self) -> str:
        return "There was an error while calling the ClimaCase API\n"\
         + f"\n Status Code: {self.status_code} -> {self.text}"
