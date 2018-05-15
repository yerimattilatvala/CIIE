using UnityEngine;

public class EnemyStats : CharacterStats {

	GameObject player;
	CharacterStats playerStats;
	public GameObject blood;
    AudioSource audioSource;


	void Start(){
		player = GameObject.FindWithTag ("Player");
		playerStats = player.GetComponent<CharacterStats> ();
        audioSource = GetComponent<AudioSource>();
    
    }


    void OnCollisionEnter(Collision collision){
        
        if (collision.gameObject.tag == "Bullet") {
       
            this.TakeDamage (playerStats.damage.getValue());

			//Sangrado
			var contact = collision.contacts[0];
			var rot = Quaternion.FromToRotation(Vector3.up, contact.normal); 
			Instantiate(blood, contact.point, rot);

			Destroy (collision.gameObject);
		}
        audioSource.Play();
	}

	public override void Die ()
	{
		base.Die ();
		audioSource.Stop ();
		audioSource.enabled = false;
		GetComponent<Collider> ().enabled = false;
	}
    
}
