from celery.decorators import task

@task(name="sum_two_numbers")
def add(x, y):
    return x + y

add.apply_async(queue='high_priority', kwargs={'x': 103, 'y': 5})
add.apply_async(queue='low_priority', args=(1, 5))

add.apply_async(queue='high_priority', priority=0, kwargs={'x': 1111, 'y': 5})
add.apply_async(queue='high_priority', priority=5, kwargs={'x': 1, 'y': 9})
add.apply_async(queue='high_priority', priority=9, kwargs={'x': 10, 'y': 5})