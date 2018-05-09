using UnityEngine;

public class CharacterStats : MonoBehaviour {


    //Valores base que no podran ser modificados
    public int maxHealth = 100;
	public bool dead= false;
    //esto es para que cualquier otra clase pueda obtenerlo (get) 
    //pero solo se pueda setear desde aqui.
    public int currentHealth {get;private set;}

    //Stats que pueden ser modificados
    public Stat damage;
    public Stat life;

    void Awake(){
        currentHealth=maxHealth;
    }
    
    void Update(){
        if (Input.GetKeyDown(KeyCode.T))
            TakeDamage(10);
    }

    public void IncreaseHealth(int life)
    {
        if (currentHealth != maxHealth)
        {
            Debug.Log("Incremento vida a "+ transform.name + ". Antes: " + currentHealth);
            currentHealth += life;
            if (currentHealth > maxHealth)
            {
                currentHealth = maxHealth;
            }
            Debug.Log("Ahora: " + currentHealth);
        }
    }
    
    public void TakeDamage (int damage){
        currentHealth -=damage;
        Debug.Log(transform.name + " takes " + damage + " damage.");

        if(currentHealth <=0)
            Die();
    }
    

    public virtual void Die (){
        //override para cada personaje
		dead=true;
        Debug.Log(transform.name + " died.");
        
    }

	public bool isDead(){
		return dead;
	}
    
    
}
