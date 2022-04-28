from celery import shared_task


# celery -A core.celery worker --pool=solo -l INFO
# celery -A core.celery beat -l INFO

@shared_task(bind=True)
def test_celery(self):
    for i in range(10):
        print(i)
    # print("CEEEEEEEEEEEEEEELERY")
    return "DONE ThE job22"
    # return HTTPResponse("the is done")