package engtelecom.poo;

public class Email {

    private String rotulo;
    private String email;

    public Email(String rotulo, String email) {
        this.rotulo = rotulo;
        setEmail(email);
    }

    public String getRotulo() {
        return rotulo;
    }

    public void setRotulo(String rotulo) {
        this.rotulo = rotulo;
    }

    public String getEmail() {
        return email;
    }

    public boolean setEmail(String email) {

        String eRR ="^[\\w-\\+]+(\\.[\\w]+)*@[\\w-]+(\\.[\\w]+)*(\\.[a-z]{2,})$";

        if(email.matches(eRR)) {
            this.email = email;
            return true;
        } else {
            return false;
        }
    }

    @Override
    public String toString() {
        return "Email{" +
                "rotulo='" + rotulo + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}
