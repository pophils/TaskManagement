

from celery_tasks import print_name_twice, print_square

if __name__ == '__main__':
    print(print_name_twice)
    print_square.delay(20)
    print_name_twice.delay('Google brin')
    print('Done sending task.')
