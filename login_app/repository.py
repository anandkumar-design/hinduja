from .models import Failed_count
from django.db.models import F
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.models import User


class check_count():
    def check_failure_count(self,user_id):
        check_count=Failed_count.objects.filter(username_id=user_id).values()
        if check_count[0]['count']>5:
            return True

    def update_failed_count(self,user_id):
        update_count = Failed_count.objects.filter(username_id=user_id)
        if update_count.exists():
            data=update_count.update(
                count = F("count")+1
            )
            if (data)>0:
                return data
        else:
            data_1 = User.objects.filter(id=user_id).values('id')
            print(data_1)
            if data_1.exists():
                id_data = data_1[0]['id']
                create_data = Failed_count.objects.create(
                username_id = id_data,
                updated_timestamp = datetime.datetime.now(),
                count =1
                )
                if (create_data.id)>0:
                    return create_data.id
