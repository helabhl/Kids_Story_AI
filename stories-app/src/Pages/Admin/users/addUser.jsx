import PageBreadcrumb from "../../../Ccomponents/common/PageBreadCrumb";
import PersonalInformationInputs from "../../../Ccomponents/form/form-elements/personal-information-inputs";
import PaiementInformation from "../../../Ccomponents/form/form-elements/PaiementInformation";

export default function AddUserForm() {
  return (
    <div>
      <PageBreadcrumb pageTitle="Add new user" />
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        <div className="space-y-6">
          <PersonalInformationInputs />
         
        </div>
        <div className="space-y-6">
            <PaiementInformation />
             <a
        href="https://tailadmin.com/pricing"
        target="_blank"
        rel="nofollow"
        className="flex items-center justify-center p-3 font-medium text-white rounded-lg bg-brand-500 text-theme-sm hover:bg-brand-600"
      >
        save user
      </a>
        </div>
      </div>
       <a
        href="https://tailadmin.com/pricing"
        target="_blank"
        rel="nofollow"
        className="flex items-center justify-center p-3 font-medium text-white rounded-lg bg-brand-500 text-theme-sm hover:bg-brand-600"
      >
        Purchase Plan
      </a>
    </div>
  );
}
