using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof (UnityEngine.AI.NavMeshAgent))]
[RequireComponent(typeof (BossCharacter))]
[RequireComponent(typeof (CharacterStats))]


public class IABoss : MonoBehaviour {

	public UnityEngine.AI.NavMeshAgent agent { get; private set; }             // the navmesh agent required for the path finding
	public BossCharacter character { get; private set; } // the character we are controlling
	private CharacterStats stats;
	private Transform target;                                    // target to aim for
	public float lookRadius = 15f;
	public float distance=20f;
	public CharacterStats playerStats;
	public GameObject shield;
	private Vector3 pos2;
	private int lastCurrentHealth;
	private bool activate = false;


	private void Start()
	{
		// get the components on the object we need ( should not be null due to require component so no need to check )
		target=GameObject.FindGameObjectWithTag("Player").transform;
		agent = GetComponentInChildren<UnityEngine.AI.NavMeshAgent>();
		character = GetComponent<BossCharacter>();
		stats = GetComponent<CharacterStats>();
		agent.updateRotation = false;
		agent.updatePosition = true;
		playerStats = GameObject.FindWithTag ("Player").GetComponent<CharacterStats> ();
		lastCurrentHealth = stats.currentHealth;


	}

	private void Update (){
	}

	private void FixedUpdate()
	{
        
		shield.SetActive (activate);
		if (activate) {
            shield.transform.position = pos2 + new Vector3(0.0f,-0.2f,3.0f);
			shield.transform.rotation = agent.transform.rotation;
			if (!stats.isDead ()) {
				agent.transform.position = pos2;
				if ((target.transform.position.z-shield.transform.position.z) < 1) {
					activate = false;  
					lastCurrentHealth = stats.currentHealth;
					// Debug.Log("Attack");
				}
			} else {
                shield.SetActive(false);
                character.Die ();
				agent.isStopped = true;
			}
		}else {
        
			pos2 = agent.transform.position + new Vector3 (-0.3f, 11f, 3.0f);
			shield.transform.position = pos2;
			shield.transform.rotation = agent.transform.rotation;
			if (!stats.isDead ()) {
				if (target != null)
					distance = Vector3.Distance (target.position, transform.position);

				if (stats.currentHealth < (lastCurrentHealth - 30)) {
					character.Protected ();
					activate = true;
					pos2 = agent.transform.position;
					//shield.transform.localRotation *= Quaternion.Euler (0, 180, 0);
				} else if (distance <= lookRadius) {
					//pos1 = shield.transform.position;
					agent.SetDestination (target.position);
					character.Move (agent.desiredVelocity, false, false);

					//Debug.Log("Radio inside");            
					if (distance < agent.stoppingDistance) {  
						character.Attack ();
						// Debug.Log("Attack");
					}
				} else {
					agent.SetDestination (agent.transform.localPosition);
					character.Move (Vector3.zero, false, false);
					//Debug.Log("Idle");
				}
			} else {
                shield.SetActive(false);
                character.Die ();
				agent.isStopped = true;
			}
		}
	}

	public void SetTarget(Transform target)
	{
		this.target = target;
	}

	void OnDrawGizmosSelected()
	{
		Gizmos.color = Color.red;
		Gizmos.DrawWireSphere(transform.position, lookRadius);
	}


}