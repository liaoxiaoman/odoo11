# -*- encoding=utf-8 -*-
from odoo import fields, api, models
import datetime
from odoo.exceptions import ValidationError
import datetime



class dTaskTask(models.Model):
    _name = 'dtask.task'
    _description = u'任务'
    _inherit = ['mail.thread']
    _rec_name = 'task_description'

    task_description = fields.Char(u'任务描述', track_visibility='onchange')
    function_menu = fields.Char(u'功能菜单')
    performer = fields.Many2one('res.users', string=u'执行人', track_visibility='onchange')
    reviewer = fields.Many2one('res.users', string=u'审核人', track_visibility='onchange')
    deadline = fields.Date(u'计划完成时间', track_visibility='onchange')
    commit_time = fields.Datetime(u'任务提交时间')
    close_time = fields.Datetime(u'任务关闭时间')
    recent_progress = fields.Selection([('1', u'待执行'), ('1.5', u'待提交'), ('2', u'待验证'), ('3', u'关闭'),('4',u'挂起')], string=u'当前进度',
                                       track_visibility='onchange')
    priority = fields.Selection([('normal', u'普通'), ('high', u'高')], string=u'优先级', default='normal')
    task_type = fields.Selection(
        [('1', u'程序开发'), ('2', u'外围集成'), ('3', u'环境搭建'), ('4', u'研发'), ('5', u'UI设计'), ('6', u'样式实现'), ('7', u'文档与方案'),
         ('8', u'项目实施'), ('9', u'BUG解决'), ('10', u'其他')], string=u'任务分类', default='1')
    project_id = fields.Many2one('dtask.project', string=u'所属项目', ondelete='restrict')
    create_user = fields.Many2one('res.users', u'创建人', default=lambda self: self.env.uid, track_visibility='onchange')
    create_date = fields.Date(u'任务创建时间')
    remark = fields.Text(u'备注', track_visibility='onchange')
    task_attachment_ids = fields.One2many('dtask.attachment', 'task_id', string=u'文档参考')
    version = fields.Char(u'版本号')
    upgrade_date = fields.Date(u'升级日期')

    @api.onchange('performer')
    def onchange_performer(self):
        if self.performer:
            self.performer_uid = self.env['res.users'].search([('employee_id', '=', self.performer.id)])

    @api.onchange('reviewer')
    def onchange_reviewer(self):
        if self.reviewer:
            self.reviewer_uid = self.env['res.users'].search([('employee_id', '=', self.reviewer.id)])

    @api.onchange('create_user')
    def onchange_create_user(self):
        if self.create_user:
            self.create_user_uid = self.env['res.users'].search([('employee_id', '=', self.create_user.id)])

    @api.one
    def action_pass(self):
        if self.create_user.id == self.env.uid or self.reviewer.id == self.env.uid:
            self.write({'recent_progress': '3',
                        'close_time': datetime.datetime.now()})
        else:
            raise ValidationError('创建人或审核人才可以点击')

    @api.one
    def action_suspend(self):
        if self.create_user.id == self.env.uid or self.reviewer.id == self.env.uid:
            self.write({'recent_progress': '4'})
        else:
            raise ValidationError('创建人或审核人才可以点击')

    @api.one
    def action_recover(self):
        if self.create_user.id == self.env.uid or self.reviewer.id == self.env.uid:
            self.write({'recent_progress': '1'})
        else:
            raise ValidationError('创建人或审核人才可以点击')

    @api.one
    def action_reject(self):
        if self.reviewer.id == self.env.uid:
            self.write({'recent_progress': '1'})
        else:
            raise ValidationError('审核人才可以点击')

    @api.one
    def action_done(self):
        if self.performer.id == self.env.uid:
            self.write({'recent_progress': '1.5'})
        else:
            raise ValidationError('执行人才可以点击')

    @api.one
    def action_commit(self):
        if self.performer.id == self.env.uid:
            self.write({'recent_progress': '2',
                        'commit_time': datetime.datetime.now()})
        else:
            raise ValidationError('执行人才可以点击')

    @api.multi
    def unlink(self):
        for r in self:
            if not (self.user_has_groups('base.user_root') or r.create_user.id == self.env.uid):
                raise ValidationError(u'只有创建人或管理员才可以删除此任务')
        return super(dTaskTask, self).unlink()

    @api.model
    def create(self, vals):
        vals['create_date'] = datetime.date.today()
        return super(dTaskTask, self).create(vals)


    @api.multi
    def button_version_mark(self):
        value = {
            # 'domain': domain,
            'name': '版本标记',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'version_mark',
            'type': 'ir.actions.act_window',
            'context':{
                'default_project': self.ids,
                'default_version': self[0].version,
                'default_upgrade_date': self[0].upgrade_date,
            },
            'target': 'new',
        }

        return value


class version_mark(models.TransientModel):
    _name = 'version_mark'

    project = fields.Many2many('dtask.task', string=u'项目')
    version = fields.Char(u'版本号')
    upgrade_date = fields.Date(u'升级日期')

    @api.multi
    def action_affirm(self):
        version=self.version
        upgrade_date=self.upgrade_date
        desc=''
        for r in self:
            r.project.write({ 'version': version,'upgrade_date': upgrade_date})
        for p in self.project:
            desc += p.task_description + '\n'
        value = {
            # 'domain': domain,
            'name': '任务描述',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'description',
            'type': 'ir.actions.act_window',
            'context': {
                'default_description':desc
            },
            'target': 'new',
        }
        return value

class description(models.TransientModel):
    _name = 'description'

    projects = fields.Many2many('dtask.task', string=u'项目')
    description=fields.Char(string=u'任务描述')
