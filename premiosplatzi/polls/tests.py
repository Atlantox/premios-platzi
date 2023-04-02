import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice


class QuestionModelTest(TestCase):        

    def test_was_published_recently_with_old_than_yesterday_date(self):
        ''' was_published_recently returns False because the question it's 24 or more hours old '''
        old_date = timezone.now() - datetime.timedelta(days=1)
        question = Question(question_text='any', pub_date=old_date)
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_current_date(self):
        ''' was_published_recently returns True because the question was published right now '''
        current_date = timezone.now()
        question = Question(question_text='any', pub_date=current_date)
        self.assertIs(question.was_published_recently(), True)
    
    def test_was_published_recently_with_future_dates(self):
        ''' Return False because a future publish date it's not a recent date '''
        future = timezone.now() + datetime.timedelta(days=30)
        question = Question(question_text='any', pub_date=future)
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_almost_yesterday_date(self):
        ''' was_published_recently returns True because the question is inside yesterday by 1 milisecond '''
        almost_yesterday = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59, milliseconds=999)
        question = Question(question_text='any', pub_date=almost_yesterday)
        self.assertIs(question.was_published_recently(), True)

def create_question(question_text, days:int):
    '''
        Create and return a Question with the given "question_text" whose publish date
        is right now +- the "days" given (positive for questions in future,
        negative for questions in the past)
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_choice(question, choice_text):
    '''
        Create and return a Choice related to "the question" and with
        the "choice_text" given
    '''
    return Choice.objects.create(question=question, choice_text=choice_text)


class QuestionIndexView(TestCase):

    def test_no_questions(self):
        ''' If no questions in database, return a appropiate message '''
        response = self.client.get(reverse('polls:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        self.assertContains(response, 'Not polls available')

    def test_past_question(self):
        ''' The IndexView only displays questions in the past '''
        past_question = create_question('past question', -4)

        response = self.client.get(reverse('polls:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_question_list']), 1)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

    def test_future_question(self):
        ''' The IndexView not displays future questions '''

        create_question('future question', 8)

        response = self.client.get(reverse('polls:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Not polls available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_only_get_questions_from_the_past(self):
        ''' 
            If a past question and a future question are saved, the IndexView 
            just displays the past question
        '''
        
        # Inserting a future question
        create_question('future question', 5)

        # Inserting a past question
        past_question = create_question('past question', -5)
        
        response = self.client.get(reverse('polls:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_question_list']), 1) # Only returns a single question
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question]) # The question returned it's the past question

    def test_two_past_questions(self):
        ''' If two past questions are saved, IndexView must display that two questions '''
        old_question = create_question('First past cuestion', -10)
        older_question = create_question('Second past cuestion', -18)

        response = self.client.get(reverse('polls:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_question_list']), 2)
        self.assertQuerysetEqual(response.context['latest_question_list'], [old_question, older_question])

class QuestionDetailsViewTest(TestCase):
    def test_future_question(self):
        ''' The DetailsView cannot show questions whose pub_date if in the future '''

        future_question = create_question('future question', 10)
        response = self.client.get(reverse('polls:details', args=(future_question.pk,)))

        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        ''' If one question with pub_date in the past is created, DetailsView will display that question '''

        past_question = create_question('past question', -10)
        response = self.client.get(reverse('polls:details', args=(past_question.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTest(TestCase):
    def test_future_question(self):
        ''' The ResultViews cannot show the resultlts if the pub_date is in the future '''

        future_question = create_question('future question', 10)
        response = self.client.get(reverse('polls:results', args=(future_question.pk,)))

        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        ''' If one question with pub_date in the past is created, ResultViews will display that choices '''

        past_question = create_question('past question', -10)
        response = self.client.get(reverse('polls:results', args=(past_question.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)


class QuestionVoteViewTest(TestCase):
    def test_question_not_exists(self):
        '''
            Trying to vote in questions that doen't exists will return a 404 error page
        '''
        response = self.client.get(reverse('polls:vote', args=(1,)))
        self.assertEqual(response.status_code,404)

    def test_question_in_the_past_and_choice_exists(self):
        '''
            If the question is in the past and the choice exists, the user wil can vote
        '''
        question = create_question('past question', -5)
        available_choice = create_choice(question, 'available choice')
        
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.post(url, {'choice':available_choice.pk})

        self.assertEqual(response.status_code, 302)

        response = self.client.get(response.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have successfully vote')

    def test_question_in_the_past_and_choice_not_exists(self):
        '''
            An user can't vote in a available question for a choice that doen't exists
        '''
        question = create_question('past question', -1)
        available_choice = create_choice(question, 'available choice')
        
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.post(url, {'choice':available_choice.pk + 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Has escogido una opción inválida')

    def test_question_in_the_future(self):
        '''
            If a question in the future is saved, you can't vote in any 
            of that question's choices
        '''
        question = create_question('future question', 1)
        available_choice = create_choice(question, 'available choice')

        url = reverse('polls:vote', args=(question.id,))
        response = self.client.post(url, {'choice':available_choice.pk})

        self.assertEqual(response.status_code, 404)
