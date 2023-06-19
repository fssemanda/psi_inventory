context = { 'staffobj': staffobj, 'AssetObj': AssetObj}
                Emails_to_send = []
                Emails = staff.objects.filter(staffrole='Finance')
                for item in Emails:
                                Emails_to_send.append(item)
                                for mail in Emails_to_send:
                                    with open(settings.BASE_DIR + "/base/templates/base/mail.txt") as f:
                                        msg = f.read()
                                    actualmail = EmailMultiAlternatives(subject="Commodity Request Approval", body=msg,
                                                                        from_email=settings.EMAIL_HOST_USER,
                                                                        to=[mail.email, ])

                                    html_template = get_template("base/Approval_Email.html").render(context)

                                    actualmail.attach_alternative(html_template, "text/html")

                                    actualmail.send()
