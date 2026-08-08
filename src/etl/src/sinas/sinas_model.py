from typing import Literal
from patito import Model
import polars as pl
from validations.polars import validate_no_blank_strings


class SinasModel(Model):
    
    location: str
    locationID: int
    taxon: str
    taxonID: int
    eventDate: str
    habitat: str
    occurrenceStatus: Literal["", "present", "absent", "absent; present"]
    establishmentMeans: Literal["introduced", "uncertain", "vagrant", "native", "uncertain; introduced", "introduced; uncertain"]
    degreeOfEstablishment: str
    pathway: str
    datasetName: str
    bibliographicCitation: str

    ###################################################################################################
    # Validations
    ###################################################################################################
    @staticmethod
    def post_validate(df: pl.DataFrame) -> None:
        validate_no_blank_strings(df, 'location')
        
        # TODO: Add more validations
