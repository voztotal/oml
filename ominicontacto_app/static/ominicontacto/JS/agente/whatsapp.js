const modalTransferChat = $('#whatsapp-modal-transfer-chat');
const modalTemplates = $('#whatsapp-modal-templates');
const modalManagementForm = $('#whatsapp-modal-managenment-form');
const modalMediaForm = $('#whatsapp-modal-media-form');
const whatsappWrapper = $('#wrapperWhatsapp');

$(function () {
    setEventListeners();
    var tiene_whatsapp = '{{ tiene_whatsapp|safe }}';
    setWhatsappStatusIcon(tiene_whatsapp === 'True');
});

const onWhatsappTransferChatEvent = ($event) => {
    const { transfer_chat } = $event.detail;
    modalTransferChat.modal(transfer_chat === true ? 'show' : 'hide');
};

const onWhatsappTemplatesEvent = ($event) => {
    const { templates } = $event.detail;
    modalTemplates.modal(templates === true ? 'show' : 'hide');
};

const onWhatsappManagementFormEvent = ($event) => {
    const { management_form } = $event.detail;
    modalManagementForm.modal(management_form === true ? 'show' : 'hide');
};

const onWhatsappMediaFormEvent = ($event) => {
    const { media_form } = $event.detail;
    modalMediaForm.modal(media_form === true ? 'show' : 'hide');
};

const onWhatsappCloseContainerEvent = ($event) => {
    whatsappWrapper.addClass('hidden');
};

const setEventListeners = () => {
    window.document.addEventListener('onWhatsappCloseContainerEvent', onWhatsappCloseContainerEvent, false);
    window.document.addEventListener('onWhatsappTransferChatEvent', onWhatsappTransferChatEvent, false);
    window.document.addEventListener('onWhatsappTemplatesEvent', onWhatsappTemplatesEvent, false);
    window.document.addEventListener('onWhatsappManagementFormEvent', onWhatsappManagementFormEvent, false);
    window.document.addEventListener('onWhatsappMediaFormEvent', onWhatsappMediaFormEvent, false);
    $('#whatsappChat').on('click', function () {
        $('#wrapperWhatsapp').toggleClass('hidden');
        $('#wrapperWebphone').removeClass('active');
    });

    // $('#btnCloseWhatsappWrapper').on('click', function () {
    //     $('#wrapperWhatsapp').addClass('hidden');
    //     $('#wrapperWebphone').removeClass('active');
    // });
};

const setWhatsappStatusIcon = (tiene_whatsapp = false) => {
    $('#whatsappChat').css({ color: tiene_whatsapp ? '#52C159' : '#6A716A' });
};