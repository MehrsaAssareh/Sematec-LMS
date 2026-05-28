import os


CONNECTION_STRING = os.getenv(
    "SEMATEC_LMS_CONNECTION_STRING",
    "Driver={SQL Server};Server=MERIII;Database=SematecLearningManagementSystem;Trusted_Connection=yes"
)
