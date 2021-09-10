from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import permission_required
from cryptography.fernet import Fernet

# for DRF
from rest_framework import viewsets
from rest_framework import permissions
# from .serializers import UserSerializer, GroupSerializer

# Create your views here.
from .models import Server, Project
from .forms import ServerForm, ProjectForm, ProfileForm


# class LoginRequiredView(LoginRequiredMixin, generic.ListView):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'
#     model = Project
#     template_name = 'credentials/login.html'
#     success_template = 'credentials/index.html'
#     queryset = Project.objects.all(),
#
#     def get_context_data(self, **kwargs):
#         context = super(LoginRequiredView, self).get_context_data(**kwargs)
#         context['server_list'] = Server.objects.all().order_by("id")
#         context['project_list'] = Project.objects.all().order_by("id")
#         return context
#
#     def post(self, request, *args, **kwargs):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # return redirect(request.META.get('HTTP_REFERER'))
#             return render(request, self.success_template)
#         else:
#             # Return an 'invalid login' error message.
#             messages.error(request, 'Invalid Login Credentials.')
#             # return HttpResponse("Invalid Login Credentials.")
#             return render(request, self.template_name)


# def index(request):
#     server_list = Server.objects.all()
#     project_list = Project.objects.all()
#     template = loader.get_template('credentials/index.html')
#     context = {
#         'server_list': server_list,
#         'project_list': project_list
#     }
#     return HttpResponse(template.render(context, request))


def login_test(request):
    server_list = Server.objects.all()
    project_list = Project.objects.all()
    template = loader.get_template('credentials/login_test.html')
    context = {
        'server_list': server_list,
        'project_list': project_list
    }
    return HttpResponse(template.render(context, request))


class IndexView(generic.ListView):
    model = Project
    template_name = 'credentials/index.html'
    queryset = Project.objects.all(),
    hashed_password = make_password("password", salt=None, hasher='default')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['server_list'] = Server.objects.all().order_by("id")
        context['project_list'] = Project.objects.all().order_by("id")
        return context

    # def get_queryset(self):
    #     return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoginView(generic.ListView):
    # model = Project
    template_name = 'credentials/login.html'
    # success_template = 'credentials/index.html'
    queryset = Project.objects.all(),

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("indexview")
        else:
            messages.error(request, 'Invalid Login Credentials.')
            return render(request, self.template_name)


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out.')
    return redirect('login')


# def login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#     """
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#     else:
#         # Return an 'invalid login' error message.
#     """
#     return render(request, 'credentials/login.html')

class ProjectView(generic.ListView):
    model = Project
    queryset = Project.objects.all().order_by("id")
    template_name = 'credentials/project_list.html'


class ServerView(generic.ListView):
    model = Server
    template_name = 'credentials/servers.html'
    queryset = Server.objects.all().order_by('id')
    redirect_field_name = 'login'


@login_required
@permission_required('credentials.view_server')
@permission_required('credentials.view_project')
def detail(request, server_id):
    if request.user.is_authenticated:
        print('request.user.is_authenticated')

    server = get_object_or_404(Server, pk=server_id)
    project_list = Project.objects.filter(server=server_id)
    template = loader.get_template('credentials/detail.html')

    return render(request, 'credentials/detail.html', {'server': server, 'project_list':project_list})


# def project_detail(request, project_id):
#     project = get_object_or_404(Project, pk=project_id)
#     return render(request, 'credentials/projectdetail.html', {'project': project})


class ProjectDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Project
    project_form = ProjectForm
    permission_required = 'credentials.view_project'
    template_name = 'credentials/projectdetail.html'

    def get(self, request, project_id, *args, **kwargs):
        project = get_object_or_404(self.model, pk=project_id)
        return render(request, self.template_name, {'project': project} )


        # def server_form(request, server_id):
#     server = get_object_or_404(Server, pk=server_id)
#     return render(request, 'credentials/projectdetail.html', {'server': server})


# @login_required
# def server_form(request, server_id):
#     server = get_object_or_404(Server, pk=server_id)
#     project = get_object_or_404(Project, pk=server_id)
#     # s = Server.objects.get(id=2)
#     # p = Project.objects.get(id=1)
#     # s.project_set.all()
#     # p.project_set.all()
#     # selected_server = server.server_set.all()
#     # selected_project = project.project_set.all()
#     try:
#         selected_choice = server.project_set.get(pk=request.POST['choice'])
#         # selected_choice = server.project_set.get(pk=3)
#     except (KeyError, Server.DoesNotExist):
#         # Redisplay the form.
#         return render(request, 'credentials/server_form.html', {
#             'server': server,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('server_form', args=(server.id,)))
#     # return HttpResponse("You're voting on question %s." % server_id)

#


# def serverform(request):
#     if request.method == "POST":
#         form = ServerForm(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/success/')
#     else:
#         form = ServerForm(initial={'key': 'value'})
#
#     return render(request, 'form_template.html', {'serverform': serverform})


@login_required
@permission_required('credentials.add_server')
@permission_required('credentials.add_project')
def add_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Server details updated.')
            return HttpResponseRedirect('/servers/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ServerForm()

    return render(request, 'credentials/new_form.html', {'form': form})


@login_required
@permission_required('credentials.change_server')
@permission_required('credentials.change_project')
def edit_server(request, server_id):
    server = get_object_or_404(Server, pk=server_id)
    form = ServerForm(request.POST or None, instance = server)
    f = Fernet(server.key)
    decrypted_password = f.decrypt(server.password.encode()).decode()
    if request.method == 'POST':
        if "delete" in request.POST:
            server.delete()
            messages.error(request, 'Document deleted.')
        elif form.is_valid():
            form.save()

        messages.success(request, 'Server details updated.')
        return HttpResponseRedirect('/servers/')

    # if a GET (or any other method) we'll create a blank form
    else:
        f = Fernet(server.key)

        form = ServerForm(initial = {'cpu' : server.cpu,
                                    'ram' : server.ram,
                                    'storage' : server.storage,
                                    'password' : server.password,
                                    'key' : server.key,
                                    'private_ip' : server.private_ip,
                                    'public_ip' : server.public_ip,
                                    'type' : server.type,
                                    'platform_hosted' : server.platform_hosted,
                                    'owner' : server.owner,
                                    'storage_type' : server.storage_type,
                                    'online': server.online,
                                     }
                        )

    return render(request, 'credentials/server_form.html', {'form': form, 'decrypted_password': decrypted_password})


@login_required
@permission_required('credentials.change_server')
@permission_required('credentials.change_project')
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == 'POST':
        if "delete" in request.POST:
            project.delete()
            messages.error(request, 'Document deleted.')
        else:
            if form.is_valid():
                form.save()

                messages.success(request, 'Project details updated.')
                return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
        # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm(initial = {'name' : project.name,
                                      'owner_client' : project.owner_client,
                                      'start_date' : project.start_date,
                                      'end_date' : project.end_date,
                                      'server' : project.server.id
                                      }
                           )

    return render(request, 'credentials/server_form.html', {'form': form})


@login_required
@permission_required('credentials.add_server')
@permission_required('credentials.add_project')
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.save()
        messages.success(request, 'Project details updated.')
        return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm()

    return render(request, 'credentials/new_form.html', {'form': form,})


@login_required
@permission_required('credentials.add_server')
@permission_required('credentials.add_project')
def add_project_on_server(request, server_id):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.save()
        messages.success(request, 'Project details updated.')
        return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm(initial = {'server' : server_id})

    return render(request, 'credentials/new_form.html', {'form': form,})



# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

def add_image(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Profile details updated.')
            return redirect('indexview')
        else:
            print("Errors", form.errors)
    else:
        form = ProfileForm()

    return render(request, 'credentials/user_profile_form.html', {'form': form,})


# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)