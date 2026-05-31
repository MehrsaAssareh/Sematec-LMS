import os
import pyodbc
from DataAccessLayer.DatabaseConfig import CONNECTION_STRING as DB_CONNECTION_STRING


class PersonPhoto_DAL_Class:
    CONNECTION_STRING = DB_CONNECTION_STRING

    def get_person_photo(self, person_id):
        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT PhotoContent, FileName, ContentType
                FROM dbo.PersonPhoto
                WHERE PersonID = ?
            """, person_id)
            row = cursor.fetchone()

        if not row:
            return None

        return {
            'content': bytes(row.PhotoContent),
            'file_name': row.FileName,
            'content_type': row.ContentType
        }

    def save_person_photo(self, person_id, photo_content, file_name=None, content_type=None, cursor=None):
        if photo_content is None:
            return

        file_name = os.path.basename(file_name) if file_name else None
        command = """
            MERGE dbo.PersonPhoto AS target
            USING (
                SELECT
                    ? AS PersonID,
                    ? AS PhotoContent,
                    ? AS FileName,
                    ? AS ContentType
            ) AS source
                ON target.PersonID = source.PersonID
            WHEN MATCHED THEN
                UPDATE SET
                    PhotoContent = source.PhotoContent,
                    FileName = source.FileName,
                    ContentType = source.ContentType,
                    UpdatedAt = SYSUTCDATETIME()
            WHEN NOT MATCHED THEN
                INSERT (PersonID, PhotoContent, FileName, ContentType)
                VALUES (source.PersonID, source.PhotoContent, source.FileName, source.ContentType);
        """

        if cursor is not None:
            cursor.execute(command, person_id, photo_content, file_name, content_type)
            return

        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            local_cursor = connection.cursor()
            local_cursor.execute(command, person_id, photo_content, file_name, content_type)
            connection.commit()

    def delete_person_photo(self, person_id, cursor=None):
        command = "DELETE FROM dbo.PersonPhoto WHERE PersonID = ?"

        if cursor is not None:
            cursor.execute(command, person_id)
            return

        with pyodbc.connect(self.CONNECTION_STRING) as connection:
            local_cursor = connection.cursor()
            local_cursor.execute(command, person_id)
            connection.commit()

    def apply_photo_change(self, cursor, person_id, model_object):
        if getattr(model_object, 'remove_photo', False):
            self.delete_person_photo(person_id, cursor)
            return

        photo_content = getattr(model_object, 'photo_content', None)
        if photo_content is None:
            return

        self.save_person_photo(
            person_id,
            photo_content,
            getattr(model_object, 'photo_file_name', None),
            getattr(model_object, 'photo_content_type', None),
            cursor
        )
