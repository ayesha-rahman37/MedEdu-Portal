from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import (
    Subject,
    Topic,
    ExamSchedule,
    Result,
    DoctorSchedule,
    Book,
    Issue,
    ExamNotice,
    Payment,
    StudentDue,
    Salary,
    StudentRecord,
    ClassSchedule,
    OperationSchedule,
    DutySchedule,
    DutySwapRequest,
    ClinicalCase,
    Notification,
    WardPosting,
    WardSwapRequest,
    Attendance,
)

from datetime import date, time

User = get_user_model()


# ================= USER TEST =================
class UserModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="student1",
            password="1234",
            role="medical_student"
        )

    def test_user_created(self):

        self.assertEqual(
            self.user.username,
            "student1"
        )

        self.assertEqual(
            self.user.role,
            "medical_student"
        )

        self.assertTrue(
            self.user.mededu_id.startswith("MS")
        )


# ================= SUBJECT TEST =================
class SubjectTest(TestCase):

    def setUp(self):

        self.subject = Subject.objects.create(
            name="Anatomy",
            phase=1,
            course_type="MBBS"
        )

    def test_subject_created(self):

        self.assertEqual(
            self.subject.name,
            "Anatomy"
        )

    def test_slug_created(self):

        self.assertEqual(
            self.subject.slug,
            "anatomy"
        )


# ================= TOPIC TEST =================
class TopicTest(TestCase):

    def setUp(self):

        self.subject = Subject.objects.create(
            name="Physiology",
            phase=1,
            course_type="MBBS"
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            title="Heart",
            full_marks=20
        )

    def test_topic_created(self):

        self.assertEqual(
            self.topic.title,
            "Heart"
        )


# ================= EXAM SCHEDULE TEST =================
class ExamScheduleTest(TestCase):

    def setUp(self):

        self.subject = Subject.objects.create(
            name="Biochemistry",
            phase=1,
            course_type="MBBS"
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            title="Protein",
            full_marks=10
        )

        self.exam = ExamSchedule.objects.create(
            subject=self.subject,
            topic=self.topic,
            exam_type="item",
            date=date.today()
        )

    def test_exam_schedule_created(self):

        self.assertEqual(
            self.exam.exam_type,
            "item"
        )


# ================= RESULT TEST =================
class ResultTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="student2",
            password="1234",
            role="medical_student"
        )

        self.subject = Subject.objects.create(
            name="Pathology",
            phase=2,
            course_type="MBBS"
        )

        self.topic = Topic.objects.create(
            subject=self.subject,
            title="Cancer",
            full_marks=20
        )

        self.result = Result.objects.create(
            user=self.user,
            topic=self.topic,
            marks=18,
            status="clear",
            date=date.today()
        )

    def test_result_created(self):

        self.assertEqual(
            self.result.marks,
            18
        )


# ================= DOCTOR SCHEDULE TEST =================
class DoctorScheduleTest(TestCase):

    def setUp(self):

        self.doctor = User.objects.create_user(
            username="doctor1",
            password="1234",
            role="doctor"
        )

        self.schedule = DoctorSchedule.objects.create(
            doctor=self.doctor,
            duty_type="ward",
            title="Morning Round",
            date=date.today(),
            start_time=time(9, 0),
            end_time=time(11, 0),
            location="Ward 5"
        )

    def test_schedule_created(self):

        self.assertEqual(
            self.schedule.location,
            "Ward 5"
        )


# ================= BOOK TEST =================
class BookTest(TestCase):

    def setUp(self):

        self.book = Book.objects.create(
            title="Gray Anatomy",
            author="Henry Gray",
            total_copies=5,
            available_copies=5
        )

    def test_book_created(self):

        self.assertEqual(
            self.book.title,
            "Gray Anatomy"
        )


# ================= ISSUE TEST =================
class IssueTest(TestCase):

    def setUp(self):

        self.student = User.objects.create_user(
            username="student3",
            password="1234",
            role="medical_student"
        )

        self.book = Book.objects.create(
            title="Medicine",
            author="Davidson"
        )

        self.issue = Issue.objects.create(
            student=self.student,
            book=self.book,
            due_date=date.today()
        )

    def test_issue_created(self):

        self.assertFalse(
            self.issue.returned
        )


# ================= EXAM NOTICE TEST =================
class ExamNoticeTest(TestCase):

    def setUp(self):

        self.notice = ExamNotice.objects.create(
            exam_type="card",
            course="MBBS",
            phase=2,
            title="Card Exam",
            description="Exam Notice",
            date=date.today()
        )

    def test_notice_created(self):

        self.assertEqual(
            self.notice.phase,
            2
        )


# ================= PAYMENT TEST =================
class PaymentTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="student4",
            password="1234",
            role="medical_student"
        )

        self.payment = Payment.objects.create(
            user=self.user,
            amount=5000,
            method="bkash",
            purpose="Admission Fee"
        )

    def test_payment_created(self):

        self.assertEqual(
            self.payment.amount,
            5000
        )


# ================= STUDENT DUE TEST =================
class StudentDueTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="student5",
            password="1234",
            role="medical_student"
        )

        self.due = StudentDue.objects.create(
            user=self.user,
            total_due=10000
        )

    def test_due_created(self):

        self.assertEqual(
            self.due.total_due,
            10000
        )


# ================= SALARY TEST =================
class SalaryTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="doctor2",
            password="1234",
            role="doctor"
        )

        self.salary = Salary.objects.create(
            user=self.user,
            amount=50000,
            month="May",
            bank_name="DBBL",
            date=date.today()
        )

    def test_salary_created(self):

        self.assertEqual(
            self.salary.month,
            "May"
        )


# ================= STUDENT RECORD TEST =================
class StudentRecordTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="student6",
            password="1234",
            role="medical_student"
        )

        self.record = StudentRecord.objects.create(
            user=self.user,
            attendance=90,
            item_pass=True,
            card_pass=True,
            term_pass=False,
            payment_clear=True
        )

    def test_record_created(self):

        self.assertEqual(
            self.record.attendance,
            90
        )


# ================= CLASS SCHEDULE TEST =================
class ClassScheduleTest(TestCase):

    def setUp(self):

        self.faculty = User.objects.create_user(
            username="faculty1",
            password="1234",
            role="faculty"
        )

        self.schedule = ClassSchedule.objects.create(
            faculty=self.faculty,
            year="1st Year",
            subject="Anatomy",
            room="201",
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0)
        )

    def test_class_schedule_created(self):

        self.assertEqual(
            self.schedule.room,
            "201"
        )


# ================= OPERATION TEST =================
class OperationScheduleTest(TestCase):

    def setUp(self):

        self.doctor = User.objects.create_user(
            username="doctor3",
            password="1234",
            role="doctor"
        )

        self.operation = OperationSchedule.objects.create(
            doctor=self.doctor,
            patient_name="Rahim",
            disease="Appendicitis",
            room="OT-1",
            date=date.today(),
            start_time=time(8, 0),
            end_time=time(10, 0)
        )

    def test_operation_created(self):

        self.assertEqual(
            self.operation.patient_name,
            "Rahim"
        )


# ================= DUTY TEST =================
class DutyScheduleTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="intern1",
            password="1234",
            role="intern"
        )

        self.doctor = User.objects.create_user(
            username="doctor4",
            password="1234",
            role="doctor"
        )

        self.duty = DutySchedule.objects.create(
            user=self.user,
            role_type="intern",
            ward="ICU",
            date=date.today(),
            start_time=time(9, 0),
            end_time=time(1, 0),
            task="Patient Monitoring",
            doctor=self.doctor,
            round_required=True
        )

    def test_duty_created(self):

        self.assertEqual(
            self.duty.ward,
            "ICU"
        )


# ================= DUTY SWAP TEST =================
class DutySwapRequestTest(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            username="intern2",
            password="1234",
            role="intern"
        )

        self.user2 = User.objects.create_user(
            username="intern3",
            password="1234",
            role="intern"
        )

        self.doctor = User.objects.create_user(
            username="doctor5",
            password="1234",
            role="doctor"
        )

        self.duty = DutySchedule.objects.create(
            user=self.user1,
            role_type="intern",
            ward="Medicine",
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
            task="Checkup",
            doctor=self.doctor
        )

        self.swap = DutySwapRequest.objects.create(
            from_user=self.user1,
            to_user=self.user2,
            duty=self.duty
        )

    def test_swap_created(self):

        self.assertEqual(
            self.swap.status,
            "pending"
        )


# ================= CLINICAL CASE TEST =================
class ClinicalCaseTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="intern4",
            password="1234",
            role="intern"
        )

        self.case = ClinicalCase.objects.create(
            intern=self.user,
            patient_name="Karim",
            phone="01700000000",
            disease="Fever",
            history="High fever for 3 days"
        )

    def test_case_created(self):

        self.assertEqual(
            self.case.disease,
            "Fever"
        )


# ================= NOTIFICATION TEST =================
class NotificationTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="student7",
            password="1234",
            role="medical_student"
        )

        self.notification = Notification.objects.create(
            user=self.user,
            message="Payment submitted"
        )

    def test_notification_created(self):

        self.assertFalse(
            self.notification.is_read
        )


# ================= WARD POSTING TEST =================
class WardPostingTest(TestCase):

    def setUp(self):

        self.student = User.objects.create_user(
            username="student8",
            password="1234",
            role="medical_student"
        )

        self.ward = User.objects.create_user(
            username="ward1",
            password="1234",
            role="ward"
        )

        self.posting = WardPosting.objects.create(
            user=self.student,
            role_type="student",
            ward_name="Medicine",
            duty_type="Morning",
            date=date.today(),
            start_time=time(8, 0),
            end_time=time(12, 0),
            assigned_by=self.ward
        )

    def test_posting_created(self):

        self.assertEqual(
            self.posting.ward_name,
            "Medicine"
        )


# ================= WARD SWAP REQUEST TEST =================
class WardSwapRequestTest(TestCase):

    def setUp(self):

        self.student1 = User.objects.create_user(
            username="student9",
            password="1234",
            role="medical_student"
        )

        self.student2 = User.objects.create_user(
            username="student10",
            password="1234",
            role="medical_student"
        )

        self.ward = User.objects.create_user(
            username="ward2",
            password="1234",
            role="ward"
        )

        self.posting = WardPosting.objects.create(
            user=self.student1,
            role_type="student",
            ward_name="Surgery",
            duty_type="Night",
            date=date.today(),
            start_time=time(8, 0),
            end_time=time(12, 0),
            assigned_by=self.ward
        )

        self.swap = WardSwapRequest.objects.create(
            posting=self.posting,
            requested_by=self.student1,
            swap_with=self.student2,
            reason="Emergency"
        )

    def test_ward_swap_created(self):

        self.assertEqual(
            self.swap.status,
            "pending"
        )


# ================= ATTENDANCE TEST =================
class AttendanceTest(TestCase):

    def setUp(self):

        self.student = User.objects.create_user(
            username="student11",
            password="1234",
            role="medical_student"
        )

        self.subject = Subject.objects.create(
            name="Pharmacology",
            phase=3,
            course_type="MBBS"
        )

        self.attendance = Attendance.objects.create(
            student=self.student,
            subject=self.subject,
            status="present"
        )

    def test_attendance_created(self):

        self.assertEqual(
            self.attendance.status,
            "present"
        )