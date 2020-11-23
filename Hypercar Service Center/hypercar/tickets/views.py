from django.views import View
from django.http.response import HttpResponse, Http404
from django.shortcuts import redirect, render
from collections import deque


menu = {
    "change_oil": "Change oil",
    "inflate_tires": "Inflate tires",
    "diagnostic": "Get diagnostic"
}


oil_queue = deque()
tires_queue = deque()
diagnostic_queue = deque()
tickets = {
    "change_oil": oil_queue,
    "inflate_tires": tires_queue,
    "diagnostic": diagnostic_queue
    }

ticket_num = -1


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        html = "<h2>Welcome to the Hypercar Service!<h2><br /><a href='/menu'>Menu</a>"
        return HttpResponse(html)


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/welcome/")


class MenuView(View):

    def get(self, request, *args, **kwargs):

        return render(request, "tickets/get_ticket.html", context={"menu": menu})


class TicketView(View):

    def ticket_num(self):
        return len(oil_queue) + len(tires_queue) + len(diagnostic_queue)

    def waiting_time(self, queue):

        if queue == oil_queue:
            return (len(oil_queue) - 1) * 2

        elif queue == tires_queue:
            return len(oil_queue) * 2 + (len(tires_queue) - 1) * 5
        else:
            return len(oil_queue) * 2 + len(tires_queue) * 5 + (len(diagnostic_queue) - 1) * 30
    def get(self, request, service, *args, **kwargs):
        if service == "change_oil":
            oil_queue.append(self.ticket_num() + 1)
            context = {
                "ticket_num" : self.ticket_num(),
                "time": self.waiting_time(oil_queue)
            }
            return render(request, "tickets/service.html", context)
        elif service == "inflate_tires":
            tires_queue.append(self.ticket_num() + 1)
            context = {
                "ticket_num" : self.ticket_num(),
                "time": self.waiting_time(tires_queue)
            }
            return render(request, "tickets/service.html", context)
        elif service == "diagnostic":
            diagnostic_queue.append(self.ticket_num() + 1)
            context = {
                "ticket_num" : self.ticket_num(),
                "time": self.waiting_time(diagnostic_queue)
            }
            return render(request, "tickets/service.html", context)
        else:
            raise Http404


class ProcessView(View):

    def get(self, request, *args, **kwargs):
        len_tickets = [len(item) for item in tickets.values()]
        context = {
            "menu": dict(zip(menu.values(), len_tickets))
        }
        return render(request, "tickets/process.html", context)

    def post(self, request, *args, **kwargs):
        global ticket_num
        if tickets["change_oil"]:
            ticket_num = tickets["change_oil"].popleft()
        elif tickets["inflate_tires"]:
            ticket_num = tickets["inflate_tires"].popleft()
        elif tickets["diagnostic"]:
            ticket_num = tickets["diagnostic"].popleft()
        else:
            ticket_num = -1
        return redirect("/next")


class NextView(View):

    def get(self, request, *args, **kwargs):
        global ticket_num
        context = {
            "id": ticket_num
        }
        return render(request, "tickets/next.html", context)


