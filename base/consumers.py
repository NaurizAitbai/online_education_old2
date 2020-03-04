import json
import tempfile
import docker
import re

from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from base.models import Lesson, LessonTest, LessonProgress, PROGRESS_STATUS


class LessonConsumer(WebsocketConsumer):
    def connect(self):
        self.container = None
        self.accept()
    
    def disconnect(self, close_node):
        if self.container:
            try:
                self.container.stop()
            except:
                pass

    def receive(self, text_data):
        user = self.scope['user']
        lesson = Lesson.objects.get(id=self.scope['url_route']['kwargs']['lesson_id'])

        data = json.loads(text_data)


        if data['type'] == 'RUN_CODE':
            try:
                lesson_progress = LessonProgress.objects.get(lesson=lesson, user=user)
                if lesson_progress.status == PROGRESS_STATUS.NOT_STARTED or lesson_progress.status == PROGRESS_STATUS.OPEN or lesson_progress.status == PROGRESS_STATUS.STARTED:
                    lesson_progress.status = PROGRESS_STATUS.STARTED
                    lesson_progress.current_code = data['code']
                    lesson_progress.save()
            except LessonProgress.DoesNotExist:
                lesson_progress = LessonProgress.objects.create(
                    lesson=lesson,
                    user=user,
                    status=PROGRESS_STATUS.STARTED,
                    current_code=data['code']
                )

            temp_file = tempfile.NamedTemporaryFile(mode='wt')

            temp_file.write("input('')\n")
            temp_file.write(data['code'])
            temp_file.flush()

            docker_host = settings.DOCKER_HOST
            docker_port = settings.DOCKER_PORT
            terminal_url = settings.TERMINAL_URL

            client = docker.DockerClient(base_url='tcp://{}:{}'.format(docker_host, docker_port))

            if self.container:
                try:
                    self.container.stop()
                except:
                    pass
                self.container = None

            container = client.containers.run('python', command='python main.py', auto_remove=True, detach=True, stdin_open=True, tty=True, volumes={
                temp_file.name: {
                    'bind': '/main.py',
                    'mode': 'rw'
                }
            })
            self.container = container

            self.send(text_data=json.dumps({
                'type': 'RUN_CODE',
                'terminal_url': terminal_url,
                'container_id': container.id,
            }))
        elif data['type'] == 'CHECK_CODE':
            try:
                lesson_progress = LessonProgress.objects.get(lesson=lesson, user=user)
                if lesson_progress.status == PROGRESS_STATUS.NOT_STARTED or lesson_progress.status == PROGRESS_STATUS.OPEN or lesson_progress.status == PROGRESS_STATUS.STARTED:
                    lesson_progress.status = PROGRESS_STATUS.STARTED
                    lesson_progress.current_code = data['code']
                    lesson_progress.save()
            except LessonProgress.DoesNotExist:
                lesson_progress = LessonProgress.objects.create(
                    lesson=lesson,
                    user=user,
                    status=PROGRESS_STATUS.STARTED,
                    current_code=data['code']
                )

            temp_file = tempfile.NamedTemporaryFile(mode='wt')
            temp_file.write("from builtins import input as old_input\n")
            temp_file.write("def alt_input(text):\n")
            temp_file.write("    return old_input('[[[' + text + ']]]\\n')\n")
            temp_file.write("input = alt_input\n")
            temp_file.write(data['code'])
            temp_file.flush()

            docker_host = settings.DOCKER_HOST
            docker_port = settings.DOCKER_PORT
            terminal_url = settings.TERMINAL_URL

            client = docker.DockerClient(base_url='tcp://{}:{}'.format(docker_host, docker_port))

            lesson_tests = LessonTest.objects.filter(lesson=lesson)

            test_result = True

            for lesson_test in lesson_tests:
                container = client.containers.create('python', command='python main.py', stdin_open=True, volumes={
                    temp_file.name: {
                        'bind': '/main.py',
                        'mode': 'rw'
                    }
                })
                container.start()

                stdin = container.attach_socket(params={'stdin': 1, 'stream': 1})
                input_data = "{}\n".format(lesson_test.input_data).encode()
                stdin._sock.send(input_data)

                container.wait()

                stdout = container.logs()
                stdout = re.sub(r'\[\[\[.*?\]\]\]', '', stdout.decode(encoding='utf-8'))

                output_data = lesson_test.output_data.split()
                result = stdout.split()

                print(output_data)
                print(result)

                if not output_data == result:
                    test_result = False
                    break
            
            if test_result:
                lesson_progress.status = PROGRESS_STATUS.FINISHED
                lesson_progress.save()
            
            self.send(text_data=json.dumps({
                'type': 'CHECK_CODE',
                'result': test_result
            }))