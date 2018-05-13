using UnityEngine;

public class EnemyStats : CharacterStats {

	GameObject player;
	CharacterStats playerStats;
	public GameObject blood;
	private AudioSource audioSource;

	private float volLowRange = .6f;
	private float volHighRange = 1.0f;

	void Start(){
		player = GameObject.FindWithTag ("Player");
		playerStats = player.GetComponent<CharacterStats> ();
		audioSource = GetComponent<AudioSource> ();
	}


	void OnCollisionEnter(Collision collision){
		if (collision.gameObject.tag == "Bullet") {
			this.TakeDamage (playerStats.damage.getValue());

			//Sonido de impacto
			//Para variar el sonido en cada disparo
			audioSource.pitch = Random.Range (volLowRange, volHighRange);
			audioSource.Play();

			//Sangrado
			var contact = collision.contacts[0];
			var rot = Quaternion.FromToRotation(Vector3.up, contact.normal); 
			Instantiate(blood, contact.point, rot);

			Destroy (collision.gameObject);
		}
	}
    
}
