from app.models import db, CleaningSchedule, Room
from app.utils.input_validator import InputValidator

class CleaningService:
    @staticmethod
    def get_schedule_by_room(room_id):
        """Получение расписания уборки для комнаты"""
        return CleaningSchedule.query.filter_by(room_id=room_id).first()

    @staticmethod
    def update_schedule(schedule_id, data):
        """Обновление расписания уборки"""
        clean_data = InputValidator.sanitize_input(data)
        schedule = db.session.get(CleaningSchedule, schedule_id)
        
        if not schedule:
            raise ValueError("Cleaning schedule not found")
        
        if 'needs_cleaning' in clean_data:
            schedule.needs_cleaning = clean_data['needs_cleaning']
        
        if 'next_cleaning_date' in clean_data:
            schedule.next_cleaning_date = clean_data['next_cleaning_date']
        
        db.session.commit()
        return schedule