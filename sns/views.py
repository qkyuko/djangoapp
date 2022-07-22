from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from.models import Message,Friend,Group,Good
from.forms import GroupCheckForm,GroupSelectForm,\
    FriendsForm,CreateGroupForm,PostForm

# Index View
@login_required(login_url='/admin/login/')
def index(request, page=1):
    #get public user
    (public_user, public_groub) = get_public()

    #post 
    if request.method == 'POST':

        #Gruop Check Form
        checkform = GroupCheckForm(request.user, request.POST)
        glist=[]
        for item in request.POST.getlist('groups'):
            glist.append(item)
        #get message
        messages = get_your_group_message(request.user, \
            glist,page)

    #get access
    else:
        checkform = GroupCheckForm(request.user)
        gps = Group.objects.filter(owner=request.user)
        glist = [public_groub.title]
        for item in gps:
            glist.append(item.title)
        messages = get_your_group_message(request.user, glist, page)

    params = {
        'login_user':request.user,
        'contents': messages,
        'check_form': checkform,
    }
    return render(request, 'sns/index.html', params)

@login_required(login_url='/admin/login/')
def groups(request):
    friends = Friend.objects.filter(owner=request.user)

    #post 送信時の処理
    if request.method == 'POST':

        if request.POST['mode'] == '__groups_form__':
            sel_group = request.POST['groups']
            gp = Group.objects.filter(owner=request.user) \
                .filter(title=sel_group).first()
            fds = Friend.objects.filter(owner=request.user) \
                    .filter(group=gp)
            print(Friend.objects.filter(owner=request.user))

            vlist = []
            for item in fds:
                vlist.append(item.user.username)
            groupsform = GroupSelectForm(request.user, request.POST)
            friendsform = FriendsForm(request.user, \
                friends=friends, vals=vlist)

        if request.POST['mode'] == '__friends_form__':
            sel_group = request.POST['group']
            group_obj = Group.objects.filter(title=sel_group).first()
            print(group_obj)
            sel_fds = request.POST.getlist('friends')
            sel_users = User.objects.filter(username__in=sel_fds)
            fds = Friend.objects.filter(owner=request.user) \
                .filter(user__in=sel_users)
            vlist=[]
            for item in fds:
                item.group = group_obj
                item.save()
                vlist.append(item.user.username)
            messages.success(request, ' チェックされたFriendを' + \
                sel_group + 'に登録しました。')
            groupsform = GroupSelectForm(request.user, \
                {'groups':sel_group})
            friendsform = FriendsForm(request.user, \
                friends=friends, vals=vlist)

    # get access
    else:
        groupsform = GroupSelectForm(request.user)
        friendsform = FriendsForm(request.user, friends=friends, \
            vals=[])
        sel_group = '-'
    
    # 共通処理
    createform = CreateGroupForm()
    params = {
        'login_user':request.user,
        'groups_form':groupsform,
        'friends_form':friendsform,
        'create_form':createform,
        'group':sel_group,
    }
    return render(request, 'sns/groups.html', params)
#friendの追加処理
@login_required(login_url='/admin/login/')
def add(request):
    add_name = request.GET['name']
    add_user = User.objects.filter(username=add_name).first()
    if add_user == request.user:
        messages.info(request, "自分自身をFriendに追加することはできま。")
        return redirect(to='/sns')
    (public_user, public_group) = get_public()
    frd_num = Friend.objects.filter(owner=request.user) \
        .filter(user=add_user).count()
    
    if frd_num > 0:
        messages.info(request, add_name.username + \
            ' は既に追加されています。')
        return redirect(to='/sns')
    
    frd = Friend()
    frd.owner = request.user
    frd.user = add_user
    frd.group = public_group
    frd.save

    messages.success(request, add_user.username + ' を追加しました！ \
        groupページに移動して、追加したFriendをメンバーに設定してください。')
    return redirect(to='/sns')

# Groupの作成
@login_required(login_url='/admin/login/')
def creategroup(request):
    gp = Group()
    gp.owner = request.user
    gp.title = request.user.username + 'の' + request.POST['group_name']
    gp.save()
    messages.info(request, '新しいグループを作成しました。')
    return redirect(to='/sns/groups')

#message post
@login_required(login_url='/admin/login/')
def post(request):
    if request.method == 'POST':
        gr_name = request.POST['groups']
        content = request.POST['content']
        
        group = Group.objects.filter(owner=request.user) \
            .filter(title=gr_name).first()
        if group == None:
            (pub_user, group) = get_public()
        msg = Message()
        msg.owner = request.user
        msg.group = group
        msg.content = content
        msg.save()
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns')
    
    #get access
    else:
        form = PostForm(request.user)
    params = {
        'login_user':request.user,
        'form':form,
    }
    return render(request, 'sns/post.html', params)

# share
@login_required(login_url='/admin/login/')
def share(request, share_id):
    share = Message.objects.get(id=share_id)
    print(share)
    
    if request.method == 'POST':
        gr_name = request.POST['groups']
        content = request.POST['content']
        group = Group.objects.filter(owner=request.user) \
            .filter(title=gr_name).first()
        if group == None:
            (pub_user, group) = get_public()
        msg = Message()
        msg.owner = request.user
        msg.group = group
        msg.content = content
        msg.share_id = share.id
        msg.save()
        share_msg = msg.get_share()
        share_msg.share_count += 1
        share_msg.save()
        messages.success(request, 'メッセージをシェアしました！')
        return redirect(to='/sns')

    form = PostForm(request.user)
    params = {
        'login_user':request.user,
        'form':form,
        'share':share,
    }
    return render(request, 'sns/share.html', params)

#good botton
@login_required(login_url='/admin/login/')
def good(request, good_id):
    good_msg = Message.objects.get(id=good_id)
    is_good = Good.objects.filter(owner=request.user) \
        .filter(message=good_msg).count()
    if is_good > 0:
        messages.success(request, '既にメッセージにはGoodしています。')
        return redirect(to='/sns')
    
    # Messageのgood_countを１増やす
    good_msg.good_count += 1
    good_msg.save()
    # Goodを作成し、設定して保存
    good = Good()
    good.owner = request.user
    good.message = good_msg
    good.save()
    # メッセージを設定
    messages.success(request, 'メッセージにGoodしました！')
    return redirect(to='/sns')


# これ以降は普通の関数==================


# 指定されたグループおよび検索文字によるMessageの取得
def get_your_group_message(owner, glist, page):
    page_num = 3 #ページあたりの表示数
    # publicの取得
    (public_user,public_group) = get_public()
    # チェックされたGroupの取得
    groups = Group.objects.filter(Q(owner=owner) \
            |Q(owner=public_user)).filter(title__in=glist)
    # Groupに含まれるFriendの取得
    me_friends = Friend.objects.filter(group__in=groups)
    # FriendのUserをリストにまとめる
    me_users = []
    for f in me_friends:
        me_users.append(f.user)
    # UserリストのUserが作ったGroupの取得
    his_groups = Group.objects.filter(owner__in=me_users)
    his_friends = Friend.objects.filter(user=owner) \
            .filter(group__in=his_groups)
    me_groups = []
    for hf in his_friends:
        me_groups.append(hf.group)
    # groupがgroupsに含まれるか、me_groupsに含まれるMessageの取得
    messages = Message.objects.filter(Q(group__in=groups) \
        |Q(group__in=me_groups))
    # ページネーションで指定ページを取得
    page_item = Paginator(messages, page_num)
    return page_item.get_page(page)

# publicなUserとGroupを取得する
def get_public():
    public_user = User.objects.filter(username='public').first()
    public_group = Group.objects.filter \
            (owner=public_user).first()
    return (public_user, public_group)




    





                



