# -*- encoding=utf-8 -*-
from odoo import fields, api, models, tools,modules


class dTaskProjectn(models.Model):
    _name = 'dtask.project'
    _description = u'项目'
    _rec_name = 'project_name'

    project_name = fields.Char(u'项目名称')
    project_manager_id = fields.Many2one('hr.employee', string='项目经理')
    plan_ids = fields.One2many('dtask.plan', 'project_id', string=u'计划')
    project_description_ids = fields.One2many('dtask.project_description', 'project_id', string=u'项目进度描述')
    project_attachment_ids = fields.One2many('dtask.attachment', 'project_id', string=u'项目文档')
    project_task_ids = fields.One2many('dtask.task', 'project_id', string=u'任务')
    project_remarks= fields.Text(string=u'项目备注')


class dTaskAttachment(models.Model):
    _name = 'dtask.attachment'
    _description = u'附件'

    @api.model
    def _default_image(self):
        image_path = modules.get_module_resource('dTask', 'static/src/img', 'word.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    filename = fields.Char(u'文件名称')
    data = fields.Binary(u'上传/下载')
    project_id = fields.Many2one('dtask.project', string=u'项目名称')
    task_id = fields.Many2one('dtask.task', string=u'任务名称')
    description = fields.Char(u'说明')
    preview = fields.Binary(compute='_compute_preview',string=u'预览')
    default_pre = fields.Binary(default=_default_image)
    @api.multi
    @api.depends('data','filename','default_pre')
    def _compute_preview(self):
        for r in self:
            r.preview = r.data
            type = r.filename.split('.')[-1].lower()
            if type not in ['png', 'jpeg','tiff','raw','bmp','gif']:
                r.preview = r.default_pre


class dTaskProblem(models.Model):
    _name = 'dtask.problem'
    _description = u'公共模块'

    desc = fields.Char(u'描述')
    user_crea = fields.Many2one('hr.employee', string=u'创建人', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)]))
    user_comm = fields.Many2one('hr.employee', string=u'提交人')
    state = fields.Selection([('crea', u'创建'), ('ongoing', u'进行中'),('finish',u'完成')], string=u'状态',default="crea")
    note= fields.Text(u'备注')


    def button_commit(self):

        if self.state == 'ongoing':
            self.write({'state': 'finish'})
        if self.state == 'crea':
            self.write({'state': 'ongoing'})