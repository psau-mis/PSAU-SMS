from odoo import _, api, fields, models, Command
from odoo.exceptions import ValidationError,Warning

class FacultyEvaluation(models.Model):
    _name = 'faculty.evaluation'
    _rec_name = "teacher_id"
    _description = 'Faculty Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    evaluation_lines = fields.One2many('evaluation.rating.line', 'evaluation_id')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('finish', 'Finish'),
        ('cancel', 'Cancel')
    ], default='draft')

    school_year_id = fields.Many2one('esmis.school.year', required=True)
    teacher_id = fields.Many2one("hr.employee", string="Teacher")

    avg_computed_score = fields.Float(string='Final Score', compute='compute_average_score', store=True, help="Final Score of computed scores in evaluation lines.")
    final_remarks = fields.Text(string='Final Remarks', compute='compute_final_remarks', store=True, help="Final remarks based on average computed score and question ratings.")
    
    @api.depends('evaluation_lines.computed_score')
    def compute_average_score(self):
        # for record in self:
        #     total_score = 0.0
        #     count = 0
        #     for line in record.evaluation_lines:
        #         if line.computed_score:
        #             total_score += float(line.computed_score)
        #             count += 1

        #     record.avg_computed_score = total_score / count if count else 0.0

        #     if record.avg_computed_score and record.state != 'finish':
        #         record.state = 'finish'
        for record in self:
            total_score = 0.0
            count = 0
            all_scores_non_zero = True

            for line in record.evaluation_lines:
                if line.computed_score:
                    total_score += float(line.computed_score)
                    count += 1
                else:
                    all_scores_non_zero = False

            if all_scores_non_zero:
                record.avg_computed_score = total_score / count if count else 0.0

                if record.avg_computed_score and record.state != 'finish':
                    record.state = 'finish'
            else:
                record.avg_computed_score = 0.0

    @api.depends('avg_computed_score')
    def compute_final_remarks(self):
        for record in self:
            rounded_score = round(record.avg_computed_score)
            if rounded_score > 5:
                final_score = 5
            else:
                final_score = rounded_score

            remarks = ''
            question_ratings = self.env['question.ratings'].search([('rating', '=', str(final_score))])
            if question_ratings:
                remarks = ', '.join(question.rating + ': ' + question.remarks for question in question_ratings)
            record.final_remarks = remarks

    @api.constrains('teacher_id', 'school_year_id')
    def constrainst_creating_duplicate(self):

        duplicate_records = self.env['faculty.evaluation'].search([
            ('school_year_id', '=', self.school_year_id.id),
            ('teacher_id', '=', self.teacher_id.id),
            ('state', '!=', 'cancel')
        ])

        if len(duplicate_records) > 1:
            raise ValidationError(_("You've already have a record that matches school year and teacher"))

    @api.onchange('school_year_id')
    def _get_teachers(self):
        self.teacher_id = False

        teacher_id = self.env['hr.employee'].search([('job_id.name', '=', 'Teacher')])

        teacher_list = []
        for teach_id in teacher_id:
            teacher_list.append(teach_id.id)
        subject_offerings_id = self.env['esmis.subject.offerings'].search([('teacher_id', 'in', teacher_list)])

        teacher_ids = []

        for rec in subject_offerings_id:
            teacher_ids.append(rec.teacher_id.id)

        return {'domain':{'teacher_id': [('id', 'in', teacher_ids)]}}
    
    @api.onchange('teacher_id')
    def _get_students(self):
        for recs in self:
            recs.evaluation_lines = None
            if recs.teacher_id:
                enrollment_ids = self.env['esmis.enrollment'].search([
                    ('school_year_id', '=', recs.school_year_id.id),
                    ('subject_enrolled.teacher_id', '=', recs.teacher_id.id),
                    ('status', '=', 'enrolled')])
                vals = []

                for enrollment_id in enrollment_ids:
                    student_ids = self.env['res.partner'].search([('id', '=', enrollment_id.student_id.id)])
                    for rec in student_ids:
                        student_val = {
                            "student_id": rec.id,
                            "gender": rec.gender
                        }
                        vals.append((Command.create(student_val)))

                recs.update({"evaluation_lines": vals})

                for evaluation_line in recs.evaluation_lines:
                    question_ratings = []
                    questions = self.env['evaluation.questions'].search([])
                    for question in questions:
                        question_rating = {
                            'question_id': question.id,
                            'rating': False,  # Default rating value
                            'remarks': False,  # Default remarks value
                        }
                        question_ratings.append((0, 0, question_rating))
                    evaluation_line.update({'question_ratings': question_ratings})
    
    def on_start(self):
        self.write({'state': 'in_progress'})
    
    def on_finish(self):
        for rec in self.evaluation_lines:
            if rec.computed_score:
                pass
            else:
                raise ValidationError("Some Students haven't submitted evaluation")
            
        self.write({'state': 'finish'})
    
    def on_cancel(self):
        self.write({'state': 'cancel'})

class EvaluationRating(models.Model):
    _name = "evaluation.rating.line"
    _description = "Faculty Evaluation Line"
    _rec_name = 'evaluation_id'

    evaluation_id = fields.Many2one('faculty.evaluation', ondelete='cascade')
    
    student_id = fields.Many2one("res.partner", domain="[('is_student','=',True)]")
    gender = fields.Selection([('Male', 'Male'),('Female', 'Female')], string="Gender")
    total_rating = fields.Float(string="Total Rating", compute='_compute_total_rating',store=True)
    computed_score = fields.Float(string="Computed Score", compute='_compute_computed_score', store=True)
    question_ratings = fields.One2many('evaluation.question.rating', 'evaluation_line_id', string='Questions')
    is_submitted = fields.Boolean()
    comment = fields.Text('Comment')

    @api.depends('question_ratings.rating')
    def _compute_total_rating(self):
        for record in self:
            total_rating = sum(int(rating.rating) for rating in record.question_ratings)
            record.total_rating = total_rating

    @api.depends('total_rating', 'question_ratings')
    def _compute_computed_score(self):
        for record in self:
            if record.total_rating and record.question_ratings:
                computed_score = record.total_rating / len(record.question_ratings)
                record.computed_score = computed_score
            else:
                record.computed_score = 0.0  # Default value or handle empty ratings case

class EvaluationQuestions(models.Model):
    _name = 'evaluation.questions'
    _rec_name = 'evaluation_question'
    _description = 'Evaluation Questions'

    evaluation_question = fields.Char('Evaluation Question')
    
class QuestionRatings(models.Model):
    _name = 'question.ratings'
    _description = 'Question Ratings'

    rating = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
    ], string='Rating', required=True)
    remarks = fields.Char('Remarks')

class EvaluationQuestionRating(models.Model):
    _name = 'evaluation.question.rating'
    _description = 'Rating Per Question Answered'
    _rec_name = 'question_id'

    evaluation_line_id = fields.Many2one('evaluation.rating.line', String="Evaluation Line", ondelete='cascade')
    question_id = fields.Many2one('evaluation.questions', string='Question', store=True, ondelete='cascade')
    rating = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string='Rating')
    remarks = fields.Char('Remarks', compute='_compute_remarks', store=True)

    @api.depends('rating')
    def _compute_remarks(self):
        for record in self:
            remarks = ''
            question_ratings = self.env['question.ratings'].search([('rating', '=', record.rating)])
            if question_ratings:
                remarks = ', '.join(question.rating + ': ' + question.remarks for question in question_ratings)
            record.remarks = remarks