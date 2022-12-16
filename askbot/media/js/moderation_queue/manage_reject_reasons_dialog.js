/* global ModalDialog, RejectReasonEditor, RejectReasonSelector, ErrorsAlert,
 WrappedElement, getSuperClass, gettext, inherits */
var ManageRejectReasonsDialog = function () {
  ModalDialog.call(this);
  this._state = null; //'select', 'edit'
  this._topMenu = null; //decline and explain menu
};
inherits(ManageRejectReasonsDialog, ModalDialog);

ManageRejectReasonsDialog.prototype.setTopMenu = function (topMenu) {
  this._topMenu = topMenu;
}

ManageRejectReasonsDialog.prototype.setState = function (state) {
  this._state = state;

  if (!this._element) return;

  if (!this._editor || !this._selector) return;

  this._editor.reset();
  this._selector.reset();

  if (state === 'add-new-reason') {
    this._selector.hide();
    this._editor.show();
    this.setHeadingText(gettext('Add new reject reason'));
  }
  if (state === 'select') {
    this._selector.show();
    this._editor.hide();
    this.setHeadingText(gettext("Manage post flag/reject reasons"));
  } 
  if (state === 'edit') {
    this._editor.show();
    this._selector.hide();
    this.setHeadingText(gettext("Edit reject reason"));
  }
};

ManageRejectReasonsDialog.prototype.reset = function () {
  this.setState(this.getReasonsCount() > 0 ? 'select' : 'add-new-reason');
  this._errors.clear();
};

ManageRejectReasonsDialog.prototype.show = function () {
  var superClass = getSuperClass(ManageRejectReasonsDialog);
  superClass.show.call(this);
  this.setState(this.getReasonsCount() > 0 ? 'select' : 'add-new-reason');
};

ManageRejectReasonsDialog.prototype.setErrors = function (errors) {
  this._errors.setErrors(errors);
};


/**
 * add/update reason in data store
 * add/update reason in the select box
 * select added reason in the select box
 */
ManageRejectReasonsDialog.prototype.setReason = function (data) {
  /* code below is draft
  
    var id = data.reason_id;
    var title = data.title;
    var details = data.details;
    this._select_box.addItem(id, title, details);

    askbot.data.postRejectReasons.push(
        {id: data.reason_id, title: data.title}
    );
    $.each(this._postModerationControls, function (idx, control) {
        control.addReason(data.reason_id, data.title);
    });
  */
};

ManageRejectReasonsDialog.prototype.getReasonsCount = function () {
  return this._selector.getReasonsCount();
};


ManageRejectReasonsDialog.prototype.createDom = function () {
  var superClass = getSuperClass(ManageRejectReasonsDialog);
  superClass.createDom.call(this);
  this._element.addClass("js-manage-reject-reasons-dialog");

  this.hideAcceptButton();
  this.hideRejectButton();

  var errors = new ErrorsAlert();
  this.appendContent(errors.getElement());
  this._errors = errors;

  var editor = new RejectReasonEditor();
  this.appendContent(editor.getElement());
  editor.setMenu(this);
  this._editor = editor;

  var selector = new RejectReasonSelector();
  selector.setMenu(this);
  this.appendContent(selector.getElement());
  this._selector = selector;
  this.setState(this.getReasonsCount() > 0 ? 'select' : 'add-new-reason');
  this._element.find('.js-modal-footer').hide();
};
