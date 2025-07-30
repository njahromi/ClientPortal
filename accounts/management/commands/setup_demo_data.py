from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Tenant, UserProfile
from clients.models import Client
from tasks.models import Task
from documents.models import Document
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Set up demo data for ClientPortal'

    def handle(self, *args, **options):
        self.stdout.write('Setting up demo data...')
        
        # Create a demo tenant
        tenant, created = Tenant.objects.get_or_create(
            name='Demo Company',
            slug='demo-company',
            defaults={'is_active': True}
        )
        if created:
            self.stdout.write(f'Created tenant: {tenant.name}')
        
        # Get or create superuser
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user')
        
        # Create user profile for admin
        profile, created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'tenant': tenant,
                'role': 'admin',
                'phone': '+1-555-0123'
            }
        )
        if created:
            self.stdout.write(f'Created user profile for {admin_user.username}')
        
        # Create demo clients
        clients_data = [
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john.smith@acme.com',
                'phone': '+1-555-0101',
                'company': 'Acme Corporation',
                'status': 'active',
                'notes': 'Key client with ongoing projects.'
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah.johnson@techstart.com',
                'phone': '+1-555-0102',
                'company': 'TechStart Inc',
                'status': 'active',
                'notes': 'Startup client, very responsive.'
            },
            {
                'first_name': 'Michael',
                'last_name': 'Brown',
                'email': 'michael.brown@globaltech.com',
                'phone': '+1-555-0103',
                'company': 'GlobalTech Solutions',
                'status': 'prospect',
                'notes': 'Potential client, needs follow-up.'
            },
            {
                'first_name': 'Emily',
                'last_name': 'Davis',
                'email': 'emily.davis@innovate.com',
                'phone': '+1-555-0104',
                'company': 'Innovate Labs',
                'status': 'active',
                'notes': 'Innovative company, great partnership potential.'
            },
            {
                'first_name': 'David',
                'last_name': 'Wilson',
                'email': 'david.wilson@legacy.com',
                'phone': '+1-555-0105',
                'company': 'Legacy Systems',
                'status': 'inactive',
                'notes': 'Former client, may reactivate.'
            }
        ]
        
        clients = []
        for client_data in clients_data:
            client, created = Client.objects.get_or_create(
                email=client_data['email'],
                tenant=tenant,
                defaults={
                    **client_data,
                    'created_by': admin_user
                }
            )
            if created:
                self.stdout.write(f'Created client: {client.full_name}')
            clients.append(client)
        
        # Create demo tasks
        tasks_data = [
            {
                'title': 'Website Redesign',
                'description': 'Complete redesign of client website with modern UI/UX',
                'status': 'in_progress',
                'priority': 'high',
                'due_date': timezone.now() + timedelta(days=14)
            },
            {
                'title': 'SEO Optimization',
                'description': 'Improve search engine rankings and organic traffic',
                'status': 'pending',
                'priority': 'medium',
                'due_date': timezone.now() + timedelta(days=7)
            },
            {
                'title': 'Content Strategy',
                'description': 'Develop comprehensive content marketing strategy',
                'status': 'completed',
                'priority': 'medium',
                'due_date': timezone.now() - timedelta(days=3)
            },
            {
                'title': 'Social Media Setup',
                'description': 'Set up and optimize social media accounts',
                'status': 'pending',
                'priority': 'low',
                'due_date': timezone.now() + timedelta(days=21)
            },
            {
                'title': 'Analytics Implementation',
                'description': 'Install and configure Google Analytics tracking',
                'status': 'in_progress',
                'priority': 'high',
                'due_date': timezone.now() + timedelta(days=5)
            }
        ]
        
        for i, task_data in enumerate(tasks_data):
            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                client=clients[i % len(clients)],
                tenant=tenant,
                defaults={
                    **task_data,
                    'created_by': admin_user,
                    'assigned_to': admin_user
                }
            )
            if created:
                self.stdout.write(f'Created task: {task.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Demo data setup completed successfully!')
        )
        self.stdout.write(f'Created {len(clients)} clients and {len(tasks_data)} tasks')
        self.stdout.write('Login with admin/admin123 to access the system') 