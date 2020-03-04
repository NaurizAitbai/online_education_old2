import json
import tempfile
import docker

from channels.generic.websocket import WebsocketConsumer
from django.conf import settings


class LessonConsumer(WebsocketConsumer):
    def connect(self):
        self.docker = None
        self.accept()
    
    def disconnect(self, close_node):
        if self.docker:
            self.docker.stop()

    def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'RUN_CODE':
            temp_file = tempfile.NamedTemporaryFile(mode='wt')

            print(data)

            temp_file.write(data['code'])
            temp_file.flush()

            docker_host = settings.DOCKER_HOST
            docker_port = settings.DOCKER_PORT
            terminal_url = settings.TERMINAL_URL

            client = docker.DockerClient(base_url='tcp://{}:{}'.format(docker_host, docker_port))

            container = client.containers.run('python', command='python main.py', auto_remove=True, detach=True, stdin_open=True, tty=True, volumes={
                temp_file.name: {
                    'bind': '/main.py',
                    'mode': 'rw'
                }
            })

            self.send(text_data=json.dumps({
                'type': 'RUN_CODE',
                'terminal_url': terminal_url,
                'container_id': container.id,
            }))
