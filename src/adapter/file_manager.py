#### File management ####
import os

#File constants#
INTERVIEW = "intervju"
REFERENCE = "referens"
CV = "cv"
TRANSCRIPT = "trancript"

UPLOAD_FOLDER = "data/input"
DOWNLOAD_FOLDER = "data/output" 

##File uploader##
def write_file_to_storage(file_data, filename, destination_folder): 
    """Sparar fil-data till angiven mapp"""
    # Create full file path for storage
    file_path = os.path.join(destination_folder, filename)

    # Validera filtyp
    # Validera storlek  
    # Error handling
    
    # Spara fil
    with open(file_path, 'wb') as f:
        f.write(file_data)
    
    # return path to file
    return file_path
   
    
    


"""
def save_multiple_files(file_list, upload_folder, destination_fold):
    saved_paths = []
    for file_data, filename in file_list:
        path = save_single_file(file_data, filename, upload_folder, ...) 
        saved_paths.append(path)
    return saved_paths
""" 

## File saving ##
def create_output_path(download_folder, candidate_name, doc_type="sammanfattning"):
    """Generate output file path"""
    filename = f"{doc_type}_{candidate_name.lower().replace(' ', '_')}.docx"
    return os.path.join(download_folder, filename)

  

    






