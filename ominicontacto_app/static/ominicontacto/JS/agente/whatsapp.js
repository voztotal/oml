const modalTransferChat = $('#whatsapp-modal-transfer-chat');
const modalTemplates = $('#whatsapp-modal-templates');
const modalManagementForm = $('#whatsapp-modal-managenment-form');
const modalMediaImageForm = $('#whatsapp-modal-media-image-form');
const modalMediaFileForm = $('#whatsapp-modal-media-file-form');
const whatsappWrapper = $('#wrapperWhatsapp');

$(function () {
    setEventListeners();
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
    const { media_form, fileType } = $event.detail;
    if (media_form) {
        if (fileType === 'img') {
            modalMediaImageForm.modal('show');
        } else {
            modalMediaFileForm.modal('show');
        }
    } else {
        modalMediaFileForm.modal('hide');
        modalMediaImageForm.modal('hide');
    }
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