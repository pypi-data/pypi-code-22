import rules

from pretalx.person.permissions import is_orga, is_reviewer, is_superuser
from pretalx.submission.permissions import is_review_author

rules.add_perm('orga.view_orga_area', is_orga | is_reviewer)
rules.add_perm('orga.search_all_users', is_orga)
rules.add_perm('orga.change_settings', is_orga)
rules.add_perm('orga.view_submission_cards', is_orga)
rules.add_perm('orga.edit_cfp', is_orga)
rules.add_perm('orga.view_question', is_orga)
rules.add_perm('orga.edit_question', is_orga)
rules.add_perm('orga.remove_question', is_orga)
rules.add_perm('orga.view_submission_type', is_orga)
rules.add_perm('orga.edit_submission_type', is_orga)
rules.add_perm('orga.remove_submission_type', is_orga)
rules.add_perm('orga.view_mails', is_orga)
rules.add_perm('orga.send_mails', is_orga)
rules.add_perm('orga.purge_mails', is_orga)
rules.add_perm('orga.view_mail_templates', is_orga)
rules.add_perm('orga.edit_mail_templates', is_orga)
rules.add_perm('orga.view_review_dashboard', is_orga | is_reviewer)
rules.add_perm('orga.view_reviews', is_reviewer)
rules.add_perm('orga.remove_review', is_superuser | is_review_author)
rules.add_perm('orga.view_schedule', is_orga)
rules.add_perm('orga.release_schedule', is_orga)
rules.add_perm('orga.edit_schedule', is_orga)
rules.add_perm('orga.schedule_talk', is_orga)
rules.add_perm('orga.view_room', is_orga)
rules.add_perm('orga.edit_room', is_orga)
rules.add_perm('orga.view_speakers', is_orga)
rules.add_perm('orga.change_speaker', is_orga)
rules.add_perm('orga.view_submissions', is_orga | is_reviewer)
rules.add_perm('orga.create_submission', is_orga)
