function TasksViewModel() {
    // idiom in JS functions, save the original value of this
    // so that callbacks, which may have a different this, can use it
    var self = this;
    self.tasksURI = 'http://localhost:5000/todo/api/v1.0/tasks'
    self.username = 'xiang'
    self.password = 'python'
    self.tasks = ko.observableArray();

    self.ajax = function(uri, method, data) {
        var request = {
            url: uri,
            type: method,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: 'json',
            data: JSON.stringify(data),
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization",
                                    "Basic" + btoa(self.username + 
                                                   ":" + self.password));
            },
            error: function(jqXHR) {
                console.log("ajax error " + jqXHR.status)
            }
        };

        return $.ajax(request);
    }

    self.beginAdd = function() {
        $("#add").modal('show');
    }
    self.beginEdit = function(task) {
        alert("Edit: " + task.title());
    }
    self.remove = function(task) {
        alert("Remove: " + task.title());
    }
    self.markInProgress = function(task) {
        task.done(false);
    }
    self.markDone = function(task) {
        task.done(true);
    }

    self.ajax(self.tasksURI, 'GET').done(function(data) {
        for (var i = 0; i < data.tasks.length; i++) {
            self.tasks.push({
                uri: ko.observable(data.tasks[i].uri),
                title: ko.observable(data.tasks[i].title),
                description: ko.observable(data.tasks[i].description),
                done: ko.observable(data.tasks[i].done)
            });
        } 
    });
}

function AddTaskViewModel() {
    var self = this;
    self.title = ko.observable();
    self.description = ko.observable();

    self.addTask = function() {
        $("#add").modal('hide');
        tasksViewModel.add({
            title: self.title(),
            descript: self.description()
        });
        self.title("");
        self.description("");
    }

}

var tasksViewModel = new TasksViewModel();
var addTaskViewModel = new AddTaskViewModel();
ko.applyBindings(tasksViewModel, $("#main")[0]);
ko.applyBindings(addTaskViewModel, $("#add")[0]);


