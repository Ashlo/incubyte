def create_sample_data(filepath: str):
    """Create a sample vaccination data file"""
    data = """|H|Customer_Name|Customer_Id|Open_Date|Last_Consulted_Date|Vaccination_Id|Dr_Name|State|Country|DOB|Is_Active
|D|Alex|123457|20101012|20231213|MVD|Paul|SA|USA|19870603|A
|D|John|123458|20101012|20231115|MVD|Paul|TN|IND|19900815|A
|D|John|123458|20101012|20231220|MVD|Sarah|VIC|AUS|19900815|A
|D|Mathew|123459|20101012|20230513|MVD|Paul|WAS|PHIL|19850421|A
|D|Matt|12345|20101012|20231201|MVD|Paul|BOS|USA|19920711|A
|D|Jacob|1256|20101012|20231225|MVD|Paul|VIC|AUS|19880305|A"""
    
    with open(filepath, 'w') as f:
        f.write(data) 