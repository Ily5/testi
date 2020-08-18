from model.record_entity import RecordEntity, RecordEntityFile
import allure
from fixture.page import generate


@allure.feature("Работа с record entities")
@allure.story("Создание сущности")
def test_create_record_entity(app):
    app.page.create_record_entity(RecordEntity(generate("Test_entity_"), "Test_value", "Test_description"))
    app.page.add_file_to_entity(RecordEntityFile(f=r"/home/ilya/docs/73.wav", f_txt=generate("file_ "), f_flag="test"))


@allure.feature("Работа с record entities")
@allure.story("Удаление сущности")
def test_delete_in_entity(app):
    app.page.delete_record_entity()
