from fastapi import APIRouter
from backend.database import get_connection
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor
from backend.models import Mlff_Data
import re
from typing import List

router = APIRouter()

@router.get("/compare-plates")
async def get_data():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Perform a JOIN query to match rows by serial_num
    query = """
        SELECT 
            a.serial_num AS serial_num,
            a.vehicle_plate_number AS plate1,
            f.vehicle_registration_number AS plate2,
            a.id AS anpr_id
        FROM 
            Anpr_data a
        LEFT JOIN 
            fastag_data f
        ON 
            a.serial_num = f.serial_num
    """
    cursor.execute(query)
    data = cursor.fetchall()

    # Regex pattern for a valid plate
    valid_plate_pattern = r"^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$"

    # Process the data and determine the status
    result = []
    for row in data:
        serial_num = row["serial_num"]
        plate1 = row["plate1"]
        plate2 = row["plate2"]
        row_id = row["anpr_id"]

        if plate1 and plate2 and plate1 == plate2:  # VRN = OCR
            status = "white"
        elif (
            plate1 and plate2 
            and plate1 != plate2 
            and re.fullmatch(valid_plate_pattern, plate1) 
            and re.fullmatch(valid_plate_pattern, plate2)
        ):   # VRN != OCR
            status = "black"
        elif not plate1:  # Box is empty
            status = "ANPR not captured"
        elif plate1 and not re.fullmatch(valid_plate_pattern, plate1):  # OCR not fully detected
            status = "OCR not fully detected"
        else:
            status = "Unknown"

        # Update the status in the Anpr_data table
        update_query = "UPDATE Anpr_data SET status = %s WHERE serial_num = %s"
        cursor.execute(update_query, (status, serial_num))

        # Append result for API response
        result.append({
            "serial_num": serial_num,
            "file1_plate": plate1,
            "file2_plate": plate2,
            "status": status
        })

    conn.commit()
    cursor.close()
    conn.close()

    return result


# @router.get ("/compare-plates")
# async def get_data ():
#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)

#     query1 = "SELECT serial_num, vehicle_plate_number FROM Anpr_data"
#     cursor.execute(query1)
#     file1_data = cursor.fetchall()

#     print(file1_data)

#     query2 = "SELECT serial_num, vehicle_registration_number FROM fastag_data"
#     cursor.execute(query2)
#     file2_data = cursor.fetchall()

   

#     file1_list = [{"serial": item["serial_num"], "plate": item["vehicle_plate_number"]} for item in file1_data]
#     file2_list = [item['vehicle_registration_number'] for item in file2_data]

#     valid_plate_pattern = r"^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$"

#     result = []
#     for file1, plate2 in zip(file1_list, file2_list):
#         plate1 = file1["plate"]
#         row_id = file1["id"]

#         if plate1 and plate2 and plate1 == plate2:  # VRN = OCR
#             status = "white"
#         elif (
#             plate1 and plate2 
#             and plate1 != plate2 
#             and re.fullmatch(valid_plate_pattern, plate1) 
#             and re.fullmatch(valid_plate_pattern, plate2)
#         ):   # VRN != OCR
#             status = "black"
#         elif not plate1:  # Box is empty
#             status = "ANPR not captured"
#         elif plate1 and not re.fullmatch(valid_plate_pattern, plate1):  # OCR not fully detected
#             status = "OCR not fully detected"
#         else:
#             status = "Unknown"

#         print(status)

#         update_query = "UPDATE Anpr_data SET status = %s WHERE id = %s"
#         cursor.execute(update_query, (status, row_id))
#         result.append({
#             "file1_plate": plate1,
#             "file2_plate": plate2,
#             "Status": status
#         })

#     conn.commit()
#     cursor.close()
#     conn.close()

#     return result

@router.get("/get-mlff-data", response_model = List[Mlff_Data])
async def get_mlff_data():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
        SELECT 
            a.serial_num, 
            a.id, 
            a.date_time, 
            a.vehicle_name, 
            a.colour, 
            a.lane_camera_id, 
            a.vehicle_plate_number,
            a.status,
            a.vehicle_image,
            a.number_plate_image, 
            f.fastag_id,
            f.vehicle_registration_number
        FROM 
            Anpr_data a
        LEFT JOIN 
            fastag_data f 
        ON 
            a.serial_num = f.serial_num
        ORDER BY 
            a.serial_num;
    """
    cursor.execute(query)
    combined_data = cursor.fetchall()


    # query2 = "Select serial_num, vehicle_registration_number from fastag_data"
    # cursor.execute(query2)
    # table2_data = cursor.fetchall()

    # print(table2_data)

    # combined_data = table1_data + table2_data

    # combined_data = []
    # for row in table1_data:
    #     combined_data.append({
    #         "id": row["id"],
    #         "date_time": row["date_time"],
    #         "vehicle_name": row["vehicle_name"],
    #         "image_path": row["image_path"],
    #         "colour": row["colour"],
    #         "lane_camera_id": row["lane_camera_id"],
    #         "vehicle_registration_number": table2_data[row["id"] - 1]["vehicle_registration_number"] if row["id"] <= len(table2_data) else "N/A",
    #         "status": row["status"]
    #     })

    # combined_data = []
    # for row in table1_data + table2_data:
    #     combined_data.append({
    #         "id": row.get("id", 0),
    #         "date_time": row.get("date_time", "N/A"),
    #         "vehicle_name": row.get("vehicle_name", "Unknown"),
    #         "image_path": row.get("image_path", "N/A"),
    #         "color": row.get("color", "Unknown"),
    #         "lane_camera_id": row.get("lane_camera_id", "N/A"),
    #         "vrn": row.get("vrn", "N/A"),
    #         "status": row.get("status", "Unknown"),
    #     })

    cursor.close()
    conn.close()

    return combined_data


