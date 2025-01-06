from pydantic import BaseModel
from datetime import datetime

class Anpr_Data(BaseModel):
    id : int
    date_time : datetime
    vehicle_id : int
    vehicle_class_id : int
    vehicle_name :str
    audited_class: str
    direction: int
    cross_line: int
    x1_coords: int
    y1_coords: int
    x2_coords: int
    y2_coords: int
    frame_number: int
    image_path: str
    color: str
    play_stream_id: int
    is_audit: int
    kit_id: int
    last_modified: str
    lane_camera_id: int
    vehicle_plate_number: str


class fastag_data (BaseModel):
    FASTag_ID: str                     
    Name: str                    
    Vehicle_Name: str                      
    Vehicle_Colour: str                      
    Vehicle_Registration_Number: str 
    Mobile_Number: str                      
    Wallet_Balance: float