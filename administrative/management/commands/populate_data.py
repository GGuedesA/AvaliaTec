from django.core.management.base import BaseCommand
from accounts.models import Usuario
from administrative.models import Block, Coordination, Room, Banca, AgendamentoSala

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):
        # Create some blocks
        block1 = Block.objects.create(name='Block A')
        block2 = Block.objects.create(name='Block B')

        # Create some coordinations and associate them with blocks
        coordination1 = Coordination.objects.create(name='Coordination 1')
        coordination1.blocks.add(block1)

        coordination2 = Coordination.objects.create(name='Coordination 2')
        coordination2.blocks.add(block2)

        # Create some rooms and associate them with blocks
        room1 = Room.objects.create(name='Sala 101', block=block1)
        room2 = Room.objects.create(name='Sala 102', block=block1)
        room3 = Room.objects.create(name='Sala 201', block=block2)

        # Create some users
        user1 = Usuario.objects.create_user(
            cpf='99999999999', email='teacher12@example.com', password='senha@123',
            role=Usuario.RoleChoices.TEACHER, name='Laura Costa'
        )
        user2 = Usuario.objects.create_user(
            cpf='11122233344', email='teacher13@example.com', password='senha@123',
            role=Usuario.RoleChoices.TEACHER, name='Daricelio Soares'
        )
        user3 = Usuario.objects.create_user(
            cpf='00011122233', email='teacher14@example.com', password='senha@123',
            role=Usuario.RoleChoices.TEACHER, name='Emannuel Victor'
        )
        user4 = Usuario.objects.create_user(
            cpf='33333333333', email='teacher4@example.com', password='senha@123',
            role=Usuario.RoleChoices.TEACHER, name='João Souza'
        )
        user5 = Usuario.objects.create_user(
            cpf='44444444444', email='teacher5@example.com', password='senha@123',
            role=Usuario.RoleChoices.TEACHER, name='Catarina Silva'
        )
        user6 = Usuario.objects.create_user(
            cpf='55555555555', email='secretary@example.com', password='senha@123',
            role=Usuario.RoleChoices.SECRETARY, name='Secretary One', fk_coordination=coordination1
        )

        # Create some bancas
        banca1 = Banca.objects.create(
            orientador=user1,
            co_orientador=user2,
            sala=room1,
            block=block1,
            coordination=coordination1,
            alunos_nomes='Gabriel, Camille',
            tema='TCC sobre Django',
            tipo=Banca.TipoBanca.TCC,
            data='2025-03-15',
            horario_inicio='10:00',
            horario_fim='12:00',
            status=Banca.StatusBanca.ANALISE
        )
        banca1.professores_banca.set([user3, user4])

        # Create some agendamentos
        agendamento1 = AgendamentoSala.objects.create(
            professor=user1,
            sala=room1,
            bloco=block1,
            coordenacao=coordination1,
            materia='Matemática',
            data='2025-03-16',
            horario_inicio='08:00',
            horario_fim='10:00',
            status=AgendamentoSala.StatusAgendamento.CONFIRMADO
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))