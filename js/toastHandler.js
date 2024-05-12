toastr.options = {
    closeButton: true
};

export const displayToastMessage = async () => {
    const toastrMessage = localStorage.getItem("toastrMessage");
    if(toastrMessage){
        toastr.success(toastrMessage)
        localStorage.removeItem("toastrMessage")
    }
}