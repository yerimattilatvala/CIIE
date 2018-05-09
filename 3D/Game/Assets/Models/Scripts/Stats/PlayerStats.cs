using UnityEngine;

public class PlayerStats : CharacterStats {


	void OnCollisionEnter(Collision collision){
		Debug.Log ("COLLISION ENTRANDO A ENANA");
	}


	public override void Die ()
	{
		base.Die ();
		Debug.Log(transform.name + " died.");
	}
    
    
}
