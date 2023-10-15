from datetime import datetime
from collections import UserDict
from error_handl_decorator import CustomError
from pickle import dump, load

DATETIME_FORMAT = "%H:%M:%S %d.%m.%Y"

class Note:
    def __init__(self, text: str, tags: str) -> None:
        self.created = datetime.now()
        self.id = None
        self.text = text
        self.tags = set()
        self.add_tags(tags)

    def edit_text(self, new_text: str) -> None:
        self.text = new_text

    def add_tags(self, tags: str) -> None:
        tag_list = tags.split(" ")
        for tag in tag_list:
            if not tag:
                continue
            if not tag.startswith("#"):
                tag = "#" + tag
            self.tags.add(tag)
        
    def remowe_tag(self, tag: str) -> None:
        if tag not in self.tags:
            raise CustomError("There is no such tag!")
        self.tags.remove(tag)

    def __str__(self) -> str:
        return f'id: {self.id}\n' \
                f'created at: {self.created.strftime(DATETIME_FORMAT)}\n' \
                f'{self.text}\n' \
                f'tags: {" ".join(self.tags)}'

class NoteBook(UserDict):
    def __init__(self, file_name: str) -> None:
        self.tag_cloud = set()  #all unique tags used in notebook
        self.file_name = file_name
        self.restore()
        self.__update_tag_cloud()

    def add_note(self, note: Note) -> None:
        if note.id in self.data:
            raise CustomError("Note is already exists!")
        note.id = self.gen_id()
        self.data[note.id] = note
        self.__update_tag_cloud()
        self.save()

    def find_id(self, id: str) -> Note:
        # find note by it id
        return self.data.get(id)

    def delete_note(self, id: str) -> None:
        if id not in self.data:
            raise CustomError(f"There is no note with id {id}")
        self.data.pop(id)
        self.__update_tag_cloud()
        self.save()

    def __update_tag_cloud(self) -> None:
        for note in self.data.values():
            self.tag_cloud.update(note.tags)

    def gen_id(self):
        max = 0
        for id in self.data.keys():
            if max < int(id):
                max = int(id)
        return str(max + 1)


    def save(self):
        with open(self.file_name, "wb") as f:
            dump(self, f)

    def restore(self):
        try:
            with open(self.file_name, "rb") as f:
                restored_data = load(f)
                self.data = restored_data.data
                self.tag_cloud = restored_data.tag_cloud
        except:
            self.data = {}
        
        

    


        

