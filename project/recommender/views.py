from django.shortcuts import get_object_or_404, render
from recommender.models import Course, User, Rating
from bitarray import bitarray

def index(request):
    """
    Home page to get user input
    """
    return render(request, 'recommender/index.html')

def submitted(request):
    """
    Home page to get user input
    """
    get_rating(request)
    return render(request, 'recommender/submitted.html')

def results(request):
    """
    Based on user input, return recommendations
    """
    ###### Map the user input to feature space #####
    user_profile, user = get_user_profile(request)
    ################################################

    ###### Map the courses to feature space and get similiarity between courses and user #####
    cosine_sim, filt_course = get_cosine_sim(user_profile, user)
    ################################################    
    
    #### Given cosine similarity, return top recommendations  ###
    rec_course1, rec_course2, rec_course3, rec_course4, rec_course5 = get_top_rec(cosine_sim, filt_course)
    context = {'rec_course1': rec_course1,'rec_course2': rec_course2,'rec_course3': rec_course3,
               'rec_course4': rec_course4,'rec_course5': rec_course5, 'user': user}
    return render(request, 'recommender/results.html', context)
    ################################################    


def get_user_profile(request):
    """
    Setting user preferences for mode, level, degree, price, duration based on the input
    """
    mode = min(255, sum([int(val) for val in request.POST.getlist('cb1')]))
    level = min(255, sum([int(val) for val in request.POST.getlist('cb2')]))
    degree = min(255, sum([int(val) for val in request.POST.getlist('cb3')]))
    price = min(255, sum([int(val) for val in request.POST.getlist('cb4')]))
    #duration = min(255, sum([int(val) for val in request.POST.getlist('cb5')]))
    sector = [int(val) for val in request.POST.getlist('cb5')]

    #In case the user does not select the courses, these are the deafult courses
    default_sectors = [186, 187, 188, 190, 191]
    if len(sector)<5:
        for i in range(5-len(sector)):
            sector.append(default_sectors[i])

    ## Saving user preference
    #u = User(name=request.POST['name'], mode=mode, level=level, degree=degree, price=price, sector1=sector[0],
    #         sector2=sector[1],sector3=sector[2],sector4=sector[3],sector5=sector[4])
    u = User(age=request.POST['age'], gender=request.POST['gender'], edu=request.POST['edu'], emp=request.POST['emp'],
             mode=mode, level=level, degree=degree, price=price, sector1=sector[0],
             sector2=sector[1],sector3=sector[2],sector4=sector[3],sector5=sector[4])

    u.save()

    user_profile = '{0:08b}'.format(mode) + '{0:08b}'.format(level) + '{0:08b}'.format(degree) + \
                    '{0:08b}'.format(price) # + '{0:08b}'.format(duration) 
    return user_profile, u


def get_cosine_sim(user_profile, user):
    """
    Map the courses into feature space
    """
    filt_course=[]
    filt_course.append(Course.objects.filter(sector=user.sector1))
    filt_course.append(Course.objects.filter(sector=user.sector2))
    filt_course.append(Course.objects.filter(sector=user.sector3))
    filt_course.append(Course.objects.filter(sector=user.sector4))
    filt_course.append(Course.objects.filter(sector=user.sector5))

    #filt_course = Course.objects.filter(sector=user.sector1) | Course.objects.filter(sector=user.sector2) | \
    #   Course.objects.filter(sector=user.sector3) | Course.objects.filter(sector=user.sector4) | Course.objects.filter(sector=user.sector5) 
    #print(filt_course)

    #num_courses = filt_course.count()
    num_courses = len(filt_course[0]) + len(filt_course[1]) + len(filt_course[2]) + len(filt_course[3]) + len(filt_course[4])

    cosine_sim = [0] * 5

    for j in range(len(filt_course)):
        cosine_sim[j] = [0] * len(filt_course[j])

        for i in range(len(filt_course[j])):
            c = filt_course[j][i]  #get_object_or_404(Course, pk=i+1)

            mode = int(2**(c.mode))    ## Mode
            level = int(2**(c.level))   ## Level

            ### The course database has numerous options for the feature 'titredecerne_id'
            ### These are grouped into 6 categories
            degree = int(c.degree)  
            degree_acc = map_degree(degree)

            price = int(c.price)   ## Price
            price_acc = map_price(price)

            duration = int(2**(c.duration-1))## Duration [TODO: to be handled]

            course_profile = '{0:08b}'.format(mode) + '{0:08b}'.format(level) + '{0:08b}'.format(degree_acc) + \
                            '{0:08b}'.format(price_acc) # + '{0:08b}'.format(duration) 
            cosine_sim[j][i] = sum(bitarray(course_profile) & bitarray(user_profile))

    return cosine_sim, filt_course


def get_top_rec(cosine_sim_arr, filt_course):
    """
    Given cosine similarity, return top recommendations 
    """
    rec_course1 = []
    rec_course2 = []
    rec_course3 = []
    rec_course4 = []
    rec_course5 = []

    for j in range(5):
        cosine_sim = cosine_sim_arr[j]

        cosine_sim.sort(reverse=True)
        sorted_course = sorted(range(len(cosine_sim)), key=lambda k: cosine_sim[k])

        for i in range(min(3,len(sorted_course))):
            if j==0:
                rec_course1.append(filt_course[j][sorted_course[i]])
            elif j==1:
                rec_course2.append(filt_course[j][sorted_course[i]]) 
            elif j==2:
                rec_course3.append(filt_course[j][sorted_course[i]]) 
            elif j==3:
                rec_course4.append(filt_course[j][sorted_course[i]]) 
            elif j==4:
                rec_course5.append(filt_course[j][sorted_course[i]]) 
    return rec_course1, rec_course2, rec_course3, rec_course4, rec_course5

def get_rating(request):
    userId = request.POST['userId']
    '''
    for i in range(3):
        courseId.append(request.POST['courseId_s1c'+str(i)])
        print(courseId[i])
    rating = []
    for i in range(3):
        rating.append(request.POST['rating_s1c'+str(i)])
        print(rating[i])
    '''
    for i in range(5):
        for j in range(3):
            courseId = request.POST.get('courseId_s'+str(i)+'c'+str(j), -1)
            rating = request.POST.get('rating_s'+str(i)+'c'+str(j), 0)
             
            r = Rating(userId=userId, courseId=courseId, rating=rating)
            r.save()


def map_degree(degree):
    """
    Group titredecerne_id into 6 categories
    The course database has numerous options for the feature 'titredecerne_id'
    These are grouped into 6 categories
    """
    baccalauréat = [162,163]
    brevet_certificat  =[165,167,169,170,171,172,173,174,175,176,177,178,179]
    diplôme = [181,182,183,184]
    bachelor = [164]
    master_licence_maîtrise =[186,190,191,192,193,194,195,196,197]
    doctorat  = [185]

    if degree in baccalauréat:
        degree_acc = 1
    elif degree in brevet_certificat:
        degree_acc = 2
    elif degree in diplôme:
        degree_acc = 4
    elif degree in bachelor:
        degree_acc = 8
    elif degree in master_licence_maîtrise:
        degree_acc = 16
    elif degree in doctorat:
        degree_acc = 32
    else:
        degree_acc = 255

    return degree_acc

def map_price(price):
    """
    Map prices into 3 categories (No preference, <500CHF, <5000CHF)
    """
    if price==0 or price>5000:
        price_acc = 255
    elif price>0 and price<=500:
        price_acc = 3
    elif price>500 and price<=5000:
        price_acc = 1
    else:
        price_acc = 255

    return price_acc


